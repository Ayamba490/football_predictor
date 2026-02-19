import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:intl/intl.dart';

void main() {
  runApp(const FootballPredictorApp());
}

class FootballPredictorApp extends StatelessWidget {
  const FootballPredictorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Football Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0A1628),
        cardColor: const Color(0xFF162C46),
      ),
      home: const PredictionsScreen(),
    );
  }
}

class PredictionsScreen extends StatefulWidget {
  const PredictionsScreen({super.key});

  @override
  State<PredictionsScreen> createState() => _PredictionsScreenState();
}

class _PredictionsScreenState extends State<PredictionsScreen> {
  List<dynamic> predictions = [];
  bool isLoading = true;
  String? error;
  int selectedLeague = 0; // 0 = All leagues

  final List<Map<String, dynamic>> leagues = [
    {'id': 0, 'name': 'All Leagues', 'flag': '⚽'},
    {'id': 39, 'name': 'Premier League', 'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'},
    {'id': 140, 'name': 'La Liga', 'flag': '🇪🇸'},
    {'id': 135, 'name': 'Serie A', 'flag': '🇮🇹'},
    {'id': 78, 'name': 'Bundesliga', 'flag': '🇩🇪'},
    {'id': 2, 'name': 'Champions League', 'flag': '🏆'},
    {'id': 1, 'name': 'World Cup 2026', 'flag': '🌍'},
  ];

  final String apiUrl =
      'https://football-predictor-7xcg.onrender.com'; // ✅ Deployed on Render - works 24/7!

  @override
  void initState() {
    super.initState();
    fetchPredictions();
  }

  Future<void> fetchPredictions() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      String url = '$apiUrl/predictions';
      if (selectedLeague > 0) {
        url += '?league=$selectedLeague';
      }

      final response = await http
          .get(
            Uri.parse(url),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          predictions = data['predictions'];
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load predictions');
      }
    } catch (e) {
      setState(() {
        error = 'Error: $e\n\nMake sure the API server is running!';
        isLoading = false;
      });
    }
  }

  List<dynamic> get filteredPredictions {
    if (selectedLeague == 0) return predictions;
    return predictions.where((p) {
      final leagueName = p['league'] as String;
      if (selectedLeague == 39) return leagueName.contains('Premier');
      if (selectedLeague == 140) return leagueName.contains('La Liga');
      if (selectedLeague == 135) return leagueName.contains('Serie');
      if (selectedLeague == 78) return leagueName.contains('Bundesliga');
      if (selectedLeague == 2) return leagueName.contains('Champions');
      if (selectedLeague == 1) return leagueName.contains('World Cup');
      return true;
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    final displayPredictions = filteredPredictions;

    return Scaffold(
      appBar: AppBar(
        title: const Text('⚽ Match Predictions'),
        backgroundColor: Colors.green[700],
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: fetchPredictions,
          ),
        ],
      ),
      body: Column(
        children: [
          // League filter dropdown
          Container(
            padding: const EdgeInsets.all(16),
            color: const Color(0xFF162C46),
            child: Row(
              children: [
                const Text(
                  'League:',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0A1628),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.green, width: 2),
                    ),
                    child: DropdownButton<int>(
                      value: selectedLeague,
                      isExpanded: true,
                      underline: const SizedBox(),
                      dropdownColor: const Color(0xFF162C46),
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      items: leagues.map((league) {
                        return DropdownMenuItem<int>(
                          value: league['id'],
                          child: Text(
                            '${league['flag']} ${league['name']}',
                            style: const TextStyle(fontSize: 14),
                          ),
                        );
                      }).toList(),
                      onChanged: (value) {
                        if (value != null) {
                          setState(() {
                            selectedLeague = value;
                          });
                        }
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Match list
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : error != null
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.error_outline,
                                  size: 60, color: Colors.red),
                              const SizedBox(height: 20),
                              Text(
                                error!,
                                textAlign: TextAlign.center,
                                style: const TextStyle(fontSize: 16),
                              ),
                              const SizedBox(height: 20),
                              ElevatedButton(
                                onPressed: fetchPredictions,
                                child: const Text('Retry'),
                              ),
                            ],
                          ),
                        ),
                      )
                    : displayPredictions.isEmpty
                        ? const Center(
                            child: Text('No matches for selected league'))
                        : RefreshIndicator(
                            onRefresh: fetchPredictions,
                            child: ListView.builder(
                              padding: const EdgeInsets.all(16),
                              itemCount: displayPredictions.length,
                              itemBuilder: (context, index) {
                                return MatchCard(
                                    prediction: displayPredictions[index]);
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class MatchCard extends StatelessWidget {
  final dynamic prediction;

  const MatchCard({super.key, required this.prediction});

  @override
  Widget build(BuildContext context) {
    final homeTeam = prediction['home_team']['name'];
    final awayTeam = prediction['away_team']['name'];
    final predictionText = prediction['prediction'];
    final confidence = prediction['confidence'];
    final scorePrediction = prediction['score_prediction'];
    final reasons = prediction['reasons'] as List;
    final date = DateTime.parse(prediction['date']);
    final probabilities = prediction['probabilities'];

    Color predictionColor = Colors.green;
    if (predictionText == 'Draw') {
      predictionColor = Colors.orange;
    } else if (predictionText == 'Away Win') {
      predictionColor = Colors.blue;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // League and date
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  prediction['league'],
                  style: TextStyle(
                    color: Colors.grey[400],
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  DateFormat('EEE, MMM d • HH:mm').format(date),
                  style: TextStyle(
                    color: Colors.grey[400],
                    fontSize: 12,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Teams
            Row(
              children: [
                Expanded(
                  child: Column(
                    children: [
                      Container(
                        width: 50,
                        height: 50,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.shield, size: 30),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        homeTeam,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Column(
                    children: [
                      Text(
                        'VS',
                        style: TextStyle(
                          color: Colors.grey[500],
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        scorePrediction,
                        style: TextStyle(
                          color: predictionColor,
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    children: [
                      Container(
                        width: 50,
                        height: 50,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.shield, size: 30),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        awayTeam,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),

            const SizedBox(height: 20),
            const Divider(),
            const SizedBox(height: 12),

            // Prediction
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: predictionColor.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: predictionColor, width: 2),
              ),
              child: Column(
                children: [
                  Text(
                    '🎯 PREDICTION: $predictionText',
                    style: TextStyle(
                      color: predictionColor,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Confidence: ${confidence.toStringAsFixed(1)}%',
                    style: TextStyle(
                      color: Colors.grey[300],
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Probabilities
            Row(
              children: [
                Expanded(
                  child: _ProbabilityBar(
                    label: 'Home',
                    percentage: probabilities['home'].toDouble(),
                    color: Colors.green,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _ProbabilityBar(
                    label: 'Draw',
                    percentage: probabilities['draw'].toDouble(),
                    color: Colors.orange,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _ProbabilityBar(
                    label: 'Away',
                    percentage: probabilities['away'].toDouble(),
                    color: Colors.blue,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 16),

            // Reasons
            Text(
              '💡 Key Factors:',
              style: TextStyle(
                color: Colors.grey[300],
                fontSize: 14,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            ...reasons.map((reason) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '• ',
                        style: TextStyle(color: Colors.grey[400]),
                      ),
                      Expanded(
                        child: Text(
                          reason,
                          style: TextStyle(
                            color: Colors.grey[400],
                            fontSize: 13,
                          ),
                        ),
                      ),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }
}

class _ProbabilityBar extends StatelessWidget {
  final String label;
  final double percentage;
  final Color color;

  const _ProbabilityBar({
    required this.label,
    required this.percentage,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: percentage / 100,
            backgroundColor: Colors.grey[800],
            color: color,
            minHeight: 8,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          '${percentage.toStringAsFixed(0)}%',
          style: TextStyle(
            fontSize: 11,
            color: Colors.grey[400],
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
