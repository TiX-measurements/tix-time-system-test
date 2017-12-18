set @tix_user_id = 23;
set @tix_location_id = 37;
set @experiment_start_timestamp = '2017-12-15 01:00:00';
set @experiment_end_timestamp = '2017-12-15 06:00:00';
set @minutes_of_processed_data = 18;
set @minutes_of_speed_transition = 8;
set @experiment_start_timestamp_with_transition = timestampadd(MINUTE, @minutes_of_speed_transition, @experiment_start_timestamp);
set @experiment_end_timestamp_with_transition = timestampadd(MINUTE, @minutes_of_speed_transition, @experiment_end_timestamp);
set @seconds_lapse_between_speed_changes = 3600;


select
  *
from measure
where
  user_id = @tix_user_id and
  location_id = @tix_location_id AND
  timestamp BETWEEN @experiment_start_timestamp and @experiment_end_timestamp
;


select timestamp, created_at, timestampdiff(SECOND, timestamp, created_at)
from measure
where
  user_id = @tix_user_id and
  location_id = @tix_location_id AND
  timestamp BETWEEN @experiment_start_timestamp and @experiment_end_timestamp
;

select
  min(timestampdiff(SECOND, timestamp, created_at)),
  avg(timestampdiff(SECOND, timestamp, created_at)),
  max(timestampdiff(SECOND, timestamp, created_at))
from measure
where
  user_id = @tix_user_id and
  location_id = @tix_location_id AND
  timestamp BETWEEN @experiment_start_timestamp and @experiment_end_timestamp
;

select count(*) / (timestampdiff(MINUTE, @experiment_start_timestamp, @experiment_end_timestamp) / (@minutes_of_processed_data / 2))
from measure
where
  user_id = @tix_user_id and
  location_id = @tix_location_id AND
  timestamp BETWEEN @experiment_start_timestamp and @experiment_end_timestamp
;

select avg(abs(downUsage - expected_downUsage) / (0.01 + expected_downUsage)) * 100
from
  (SELECT
     `timestamp`,
     downUsage,
     CASE
     WHEN timestamp BETWEEN @experiment_start_timestamp_with_transition AND
                            timestampadd(SECOND, @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
       THEN 1.0
     WHEN timestamp BETWEEN timestampadd(SECOND, @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition) AND
                            timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
       THEN 0.75
     WHEN timestamp BETWEEN timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition) AND
                            timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
       THEN 0.5
     WHEN timestamp BETWEEN timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition) AND
                            timestampadd(SECOND, 4 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
       THEN 0.25
     ELSE 0.0
     END AS expected_downUsage
    FROM measure
    WHERE
      user_id = @tix_user_id and
      location_id = @tix_location_id AND
      timestamp BETWEEN @experiment_start_timestamp and @experiment_end_timestamp
  ) as t
;

SELECT avg(relative_error) AS median
FROM
  (SELECT
     @row_id := @row_id + 1 AS row_id,
     x.relative_error       AS relative_error
   FROM
     (
       SELECT
         downUsage - expected_downUsage AS                                  error,
         abs(downUsage - expected_downUsage) / (0.001 + expected_downUsage) relative_error
       FROM
         (SELECT
            `timestamp`,
            downUsage,
            CASE
            WHEN timestamp BETWEEN @experiment_start_timestamp_with_transition AND
            timestampadd(SECOND, @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
              THEN 1.0
            WHEN timestamp BETWEEN timestampadd(SECOND, @seconds_lapse_between_speed_changes,
                                                @experiment_start_timestamp_with_transition) AND
            timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
              THEN 0.75
            WHEN timestamp BETWEEN timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes,
                                                @experiment_start_timestamp_with_transition) AND
            timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
              THEN 0.5
            WHEN timestamp BETWEEN timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes,
                                                @experiment_start_timestamp_with_transition) AND
            timestampadd(SECOND, 4 * @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
              THEN 0.25
            ELSE 0.0
            END AS expected_downUsage
          FROM measure
          WHERE
            user_id = @tix_user_id AND
            location_id = @tix_location_id AND
            timestamp BETWEEN @experiment_start_timestamp AND @experiment_end_timestamp
         ) AS t
       ORDER BY relative_error
     ) x,
     (SELECT @row_id := 0) t2
  ) o,
  (
    SELECT count(*) AS total_rows
    FROM (
           SELECT
             downUsage - expected_downUsage AS                                  error,
             abs(downUsage - expected_downUsage) / (0.001 + expected_downUsage) relative_error
           FROM
             (SELECT
                `timestamp`,
                downUsage,
                CASE
                WHEN timestamp BETWEEN @experiment_start_timestamp_with_transition AND
                timestampadd(SECOND, @seconds_lapse_between_speed_changes, @experiment_start_timestamp_with_transition)
                  THEN 1.0
                WHEN timestamp BETWEEN timestampadd(SECOND, @seconds_lapse_between_speed_changes,
                                                    @experiment_start_timestamp_with_transition) AND
                timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes,
                             @experiment_start_timestamp_with_transition)
                  THEN 0.75
                WHEN timestamp BETWEEN timestampadd(SECOND, 2 * @seconds_lapse_between_speed_changes,
                                                    @experiment_start_timestamp_with_transition) AND
                timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes,
                             @experiment_start_timestamp_with_transition)
                  THEN 0.5
                WHEN timestamp BETWEEN timestampadd(SECOND, 3 * @seconds_lapse_between_speed_changes,
                                                    @experiment_start_timestamp_with_transition) AND
                timestampadd(SECOND, 4 * @seconds_lapse_between_speed_changes,
                             @experiment_start_timestamp_with_transition)
                  THEN 0.25
                ELSE 0.0
                END AS expected_downUsage
              FROM measure
              WHERE
                user_id = @tix_user_id AND
                location_id = @tix_location_id AND
                timestamp BETWEEN @experiment_start_timestamp AND @experiment_end_timestamp
             ) AS t
           ORDER BY relative_error
         ) x
  ) p
WHERE o.row_id IN (floor(p.total_rows / 2), ceil(p.total_rows / 2));
