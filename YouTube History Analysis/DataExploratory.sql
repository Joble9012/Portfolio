-- Total number of videos watched
SELECT COUNT(*) AS total_videos_watched 
FROM youtube_history;

-- Number of videos watched per channel
SELECT channel_name, COUNT(*) AS video_count  
FROM youtube_history
WHERE channel_name IS NOT NULL  
GROUP BY channel_name  
ORDER BY video_count DESC;

-- Total number of videos watched per weekday
SELECT watch_day, COUNT(*) AS video_count  
FROM youtube_history  
GROUP BY watch_day  
ORDER BY video_count DESC;

-- Top 5 most watched videos
SELECT video_title, COUNT(*) AS watch_count  
FROM youtube_history  
GROUP BY video_title  
ORDER BY watch_count DESC  
LIMIT 5;

-- Total number of videos watched per hour of the day
SELECT watch_hour, COUNT(*) AS watch_count  
FROM youtube_history  
GROUP BY watch_hour  
ORDER BY watch_hour ASC;

-- The average number of videos watched per day
SELECT ROUND(AVG(video_count),2) AS avg_videos_per_day  
FROM (SELECT watch_date, COUNT(*) AS video_count  
    FROM youtube_history  
    GROUP BY watch_date) AS daily_counts;

-- Top channel watched for each day of the week
SELECT watch_day, channel_name, video_count 
FROM (SELECT watch_day, channel_name, COUNT(*) AS video_count, 
        RANK() OVER (PARTITION BY watch_day ORDER BY COUNT(*) DESC) AS rnk  
    FROM youtube_history  
    GROUP BY watch_day, channel_name) ranked  
WHERE rnk = 1
    AND channel_name != 'ESPN';

-- Average number of videos watched per channel
SELECT ROUND(AVG(video_count),2) AS avg_videos_per_channel 
FROM (SELECT channel_name, COUNT(*) AS video_count  
    FROM youtube_history  
    GROUP BY channel_name) channel_counts;

-- Percentage of videos watched from the top 5 channels
SELECT channel_name,  
       COUNT(*) AS video_count,  
       ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM youtube_history),2) AS percentage  
FROM youtube_history  
GROUP BY channel_name  
ORDER BY video_count DESC  
LIMIT 5;

-- Word count in titles
WITH words AS (SELECT unnest(string_to_array(lower(video_title), ' ')) AS word
    FROM youtube_history)
SELECT word, COUNT(*) AS word_count
FROM words
WHERE LENGTH(word) > 3  -- Ignore short words
    AND word NOT IN ('the', 'and', 'for', 'with', 'this', 'that', 'your', 'from', 'what', 'when', 'where', 'how', 'after', 'most', 'full', 'make', 'will')
GROUP BY word
ORDER BY word_count DESC
LIMIT 20;



