-- Rolada · rànquing de família
-- Enganxa tot aquest text a Supabase > SQL Editor > New query > Run.
-- Les taules no són accessibles directament: el joc només hi parla a través
-- de les funcions de sota, i cada funció demana el codi de família.

create extension if not exists pgcrypto with schema extensions;

create table if not exists public.rolada_players (
  id uuid primary key default gen_random_uuid(),
  family_hash text not null,
  name text not null check (char_length(name) between 1 and 20),
  sail text not null default '' check (char_length(sail) <= 12),
  xp integer not null default 0 check (xp >= 0),
  wins integer not null default 0 check (wins >= 0),
  races integer not null default 0 check (races >= 0),
  stars jsonb not null default '{}'::jsonb,
  streak jsonb not null default '{}'::jsonb,
  skin text not null default 'opti' check (char_length(skin) <= 20),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists rolada_players_family_idx on public.rolada_players (family_hash);

create table if not exists public.rolada_results (
  id bigint generated always as identity primary key,
  family_hash text not null,
  player_id uuid not null references public.rolada_players (id) on delete cascade,
  kind text not null check (kind in ('level', 'daily')),
  level text not null check (char_length(level) <= 20),
  day integer,
  pos integer not null check (pos between 1 and 50),
  fleet integer not null check (fleet between 1 and 50),
  time_s real,
  created_at timestamptz not null default now()
);
create index if not exists rolada_results_family_day_idx on public.rolada_results (family_hash, day);

alter table public.rolada_players enable row level security;
alter table public.rolada_results enable row level security;
revoke all on public.rolada_players from anon, authenticated;
revoke all on public.rolada_results from anon, authenticated;

create or replace function public.rolada_fh(p_family text)
returns text language sql immutable set search_path = public, extensions as $$
  select encode(extensions.digest(upper(trim(p_family)), 'sha256'), 'hex')
$$;

create or replace function public.rolada_check(p_family text)
returns text language plpgsql immutable set search_path = public, extensions as $$
begin
  if p_family is null or char_length(trim(p_family)) < 6 then
    raise exception 'codi de família massa curt';
  end if;
  return public.rolada_fh(p_family);
end $$;

create or replace function public.rolada_players_list(p_family text)
returns table (id uuid, name text, sail text, xp integer, wins integer, races integer, stars jsonb, streak jsonb, skin text)
language sql security definer set search_path = public, extensions as $$
  select p.id, p.name, p.sail, p.xp, p.wins, p.races, p.stars, p.streak, p.skin
  from public.rolada_players p
  where p.family_hash = public.rolada_check(p_family)
  order by p.created_at
$$;

create or replace function public.rolada_join(p_family text, p_name text, p_sail text)
returns table (id uuid, name text, sail text, xp integer, wins integer, races integer, stars jsonb, streak jsonb, skin text)
language plpgsql security definer set search_path = public, extensions as $$
declare fh text := public.rolada_check(p_family);
begin
  if not exists (select 1 from public.rolada_players p where p.family_hash = fh and lower(p.name) = lower(trim(p_name))) then
    if (select count(*) from public.rolada_players p where p.family_hash = fh) >= 12 then
      raise exception 'aquesta família ja té 12 regatistes';
    end if;
    insert into public.rolada_players (family_hash, name, sail)
    values (fh, trim(p_name), upper(trim(coalesce(p_sail, ''))));
  end if;
  return query
    select p.id, p.name, p.sail, p.xp, p.wins, p.races, p.stars, p.streak, p.skin
    from public.rolada_players p
    where p.family_hash = fh and lower(p.name) = lower(trim(p_name))
    limit 1;
end $$;

create or replace function public.rolada_save(p_family text, p_id uuid, p_xp integer, p_wins integer, p_races integer, p_stars jsonb, p_streak jsonb, p_skin text)
returns void language sql security definer set search_path = public, extensions as $$
  update public.rolada_players p set
    xp = greatest(p.xp, least(p_xp, 10000000)),
    wins = greatest(p.wins, least(p_wins, 100000)),
    races = greatest(p.races, least(p_races, 100000)),
    stars = coalesce(p_stars, p.stars),
    streak = coalesce(p_streak, p.streak),
    skin = left(coalesce(p_skin, p.skin), 20),
    updated_at = now()
  where p.id = p_id and p.family_hash = public.rolada_check(p_family)
$$;

create or replace function public.rolada_result(p_family text, p_id uuid, p_kind text, p_level text, p_day integer, p_pos integer, p_fleet integer, p_time real)
returns void language sql security definer set search_path = public, extensions as $$
  insert into public.rolada_results (family_hash, player_id, kind, level, day, pos, fleet, time_s)
  select p.family_hash, p.id, p_kind, p_level, p_day, p_pos, p_fleet, p_time
  from public.rolada_players p
  where p.id = p_id and p.family_hash = public.rolada_check(p_family)
$$;

create or replace function public.rolada_board(p_family text, p_day integer)
returns table (id uuid, name text, sail text, xp integer, wins integer, races integer, stars jsonb, skin text, daily_pos integer, daily_time real)
language sql security definer set search_path = public, extensions as $$
  select p.id, p.name, p.sail, p.xp, p.wins, p.races, p.stars, p.skin, d.pos, d.time_s
  from public.rolada_players p
  left join lateral (
    select r.pos, r.time_s from public.rolada_results r
    where r.player_id = p.id and r.kind = 'daily' and r.day = p_day
    order by r.pos, r.time_s limit 1
  ) d on true
  where p.family_hash = public.rolada_check(p_family)
$$;

revoke execute on all functions in schema public from public;
grant execute on function public.rolada_players_list(text) to anon, authenticated;
grant execute on function public.rolada_join(text, text, text) to anon, authenticated;
grant execute on function public.rolada_save(text, uuid, integer, integer, integer, jsonb, jsonb, text) to anon, authenticated;
grant execute on function public.rolada_result(text, uuid, text, text, integer, integer, integer, real) to anon, authenticated;
grant execute on function public.rolada_board(text, integer) to anon, authenticated;
