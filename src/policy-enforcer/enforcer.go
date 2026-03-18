package main

import (
	"fmt"
	"log"
	"net/http"
	"encoding/json"
)

// Define the incoming data structure from the ML Predictor
type PredictionResult struct {
	CommitID       string  `json:"commit_id"`
	RiskScore      float64 `json:"risk_score"`
	PipelineAction string  `json:"pipeline_action"`
}

func enforcePolicyHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Only POST requests are allowed", http.StatusMethodNotAllowed)
		return
	}

	var result PredictionResult
	err := json.NewDecoder(r.Body).Decode(&result)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Simulate sending a status update to the GitHub API
	fmt.Printf("Received Decision for Commit: %s\n", result.CommitID)
	fmt.Printf("Risk Score: %.2f\n", result.RiskScore)
	
	switch result.PipelineAction {
	case "BLOCK":
		fmt.Println("Action: Blocking Pull Request. Risk is too high.")
	case "WARN":
		fmt.Println("Action: Adding warning comment. Requesting Senior SRE review.")
	case "APPROVE":
		fmt.Println("Action: Approving commit. Pipeline continues.")
	default:
		fmt.Println("Action: Unknown status. Defaulting to manual review.")
	}
	fmt.Println("**************************************************")

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status": "Policy Enforced on GitHub"}`))
}

func main() {
	http.HandleFunc("/enforce", enforcePolicyHandler)
	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})
	
	fmt.Println("Policy Enforcer listening on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}