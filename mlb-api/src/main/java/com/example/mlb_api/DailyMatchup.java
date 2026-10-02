package com.example.mlb_api;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDate;

// Maps the Java object to the daily_matchups db table
@Entity
@Table(name = "daily_matchups")
public class DailyMatchup {
    
    @Id
    private Integer gamePk;
    private LocalDate gameDate;
    private String awayTeam;
    private String homeTeam;
    private String awayPitcher;
    private String homePitcher;
    private BigDecimal yrfiProbability;

    // Getters
    public Integer getGamePk() { return gamePk; }
    public LocalDate getGameDate() { return gameDate; }
    public String getAwayTeam() { return awayTeam; }
    public String getHomeTeam() { return homeTeam; }
    public String getAwayPitcher() { return awayPitcher; }
    public String getHomePitcher() { return homePitcher; }
    public BigDecimal getYrfiProbability() { return yrfiProbability; }
}