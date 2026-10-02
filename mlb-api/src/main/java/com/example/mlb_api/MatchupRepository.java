package com.example.mlb_api;

import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDate;
import java.util.List;

// Interfance to automatically generate SQL queries
public interface MatchupRepository extends JpaRepository<DailyMatchup, Integer> {
    List<DailyMatchup> findByGameDate(LocalDate gameDate);
}