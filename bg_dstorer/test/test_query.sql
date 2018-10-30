--intermediate query while working on score per turn, without group
set @lt=NULL;
select b.t, b.distance, event_idx, CAST(last_t as DECIMAL) as last_t_dec, curr_t, event_type from
(
	SELECT @rn:=@rn+1 as event_idx, `t`, @lt last_t, @lt:=t curr_t, `event_type`
	from (
		select `t`, `event_type` FROM `events`
		order by `t`
	) t1, (SELECT @rn:=-1) t2
) as a
inner join distances as b
	on b.t > a.last_t
    and b.t < a.curr_t;

--query for score per turn
set @lt=NULL;
select max(b.distance), event_idx from
(
	SELECT @rn:=@rn+1 as event_idx, `t`, @lt last_t, @lt:=t curr_t, `event_type`
	from (
		select `t`, `event_type` FROM `events`
		order by `t`
	) t1, (SELECT @rn:=-1) t2
) as a
inner join distances as b
	on b.t > a.last_t
    and b.t < a.curr_t
group by event_idx;
