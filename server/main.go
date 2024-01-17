package main

import (
	"encoding/csv"
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

// Data représente la structure des données que nous voulons envoyer.
type Data struct {
	Timestamp string `json:"timestamp"`
	Value     string `json:"value"`
}

const PORT = ":8081"

func main() {
	rand.Seed(time.Now().UnixNano()) // Initialiser le générateur de nombres aléatoires
	http.HandleFunc("/data", dataHandler)
	log.Println("Serveur démarré sur : http://localhost" + PORT)
	log.Fatal(http.ListenAndServe(PORT, nil))
}

func dataHandler(w http.ResponseWriter, r *http.Request) {
	// Récupérer le format demandé, par défaut JSON
	format := r.URL.Query().Get("format")
	if format == "" {
		format = "json"
	}

	// Créer des données avec une valeur aléatoire
	data := Data{
		Timestamp: time.Now().Format("2006-01-02-15-04"),
		Value:     randomValue(),
	}

	switch format {
	case "json":
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(data)
	case "csv":
		w.Header().Set("Content-Type", "text/csv")
		writer := csv.NewWriter(w)
		defer writer.Flush()
		writer.Write([]string{data.Timestamp, data.Value})
	default:
		http.Error(w, "Format non supporté", http.StatusBadRequest)
	}
}

// randomValue génère une valeur aléatoire sous forme de chaîne de caractères.
func randomValue() string {
	// Exemple : générer un nombre aléatoire entre 0 et 99
	return strconv.Itoa(rand.Intn(100))
}
