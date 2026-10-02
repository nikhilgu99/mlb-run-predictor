package com.example.mlb_api;

import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
import java.util.List;

// A controller to handle web requests and return data as JSON payload
@RestController
@RequestMapping("/api/matchups")
@CrossOrigin(origins = "*") // Allows future React frontend to request data
public class MatchupController {

    private final MatchupRepository repository;

    public MatchupController(MatchupRepository repository) {
        this.repository = repository;
    }

    // Endpoint: http://localhost:8080/api/matchups/today
    @GetMapping("/today")
    public List<DailyMatchup> getTodayMatchups() {
        return repository.findByGameDate(LocalDate.now());
    }

    // Endpoint: http://localhost:8080/api/matchups
    @GetMapping
    public List<DailyMatchup> getAllMatchups() {
        return repository.findAll();
    }
}