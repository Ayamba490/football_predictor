"""
Flask API Server for Football Predictions
Serves predictions to mobile app
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from predictor import FootballPredictor
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Allow requests from Flutter app

# Initialize predictor
API_KEY = os.getenv('FOOTBALL_API_KEY', 'YOUR_API_KEY')
predictor = FootballPredictor(api_key=API_KEY)


@app.route('/')
def home():
    """API info"""
    return jsonify({
        'name': 'Football Match Predictor API',
        'version': '1.0',
        'endpoints': {
            '/predictions': 'GET - Get upcoming match predictions',
            '/predict': 'POST - Predict specific match',
            '/leagues': 'GET - Get available leagues'
        }
    })


@app.route('/predictions', methods=['GET'])
def get_predictions():
    """
    Get predictions for upcoming matches
    Query params: league (default: 39 = Premier League)
    """
    league_id = request.args.get('league', 39, type=int)
    
    try:
        # Fetch upcoming matches
        matches = predictor.get_upcoming_matches(league_id=league_id)
        
        # Generate predictions for each match
        predictions = []
        for match in matches:
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            
            pred = predictor.predict_match(
                home_team, 
                away_team,
                match['teams']['home']['id'],
                match['teams']['away']['id']
            )
            
            predictions.append({
                'match_id': match['fixture']['id'],
                'date': match['fixture']['date'],
                'league': match['league']['name'],
                'venue': match['fixture'].get('venue', {}).get('name', 'Unknown'),
                'home_team': {
                    'name': home_team,
                    'logo': match['teams']['home'].get('logo', '')
                },
                'away_team': {
                    'name': away_team,
                    'logo': match['teams']['away'].get('logo', '')
                },
                'prediction': pred['prediction'],
                'confidence': pred['confidence'],
                'score_prediction': pred['score_prediction'],
                'probabilities': {
                    'home': pred['home_win_prob'],
                    'draw': pred['draw_prob'],
                    'away': pred['away_win_prob']
                },
                'reasons': pred['reasons']
            })
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'predictions': predictions
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict_specific_match():
    """
    Predict a specific match
    Body: { "home_team": "...", "away_team": "..." }
    """
    data = request.get_json()
    
    if not data or 'home_team' not in data or 'away_team' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing home_team or away_team'
        }), 400
    
    try:
        pred = predictor.predict_match(
            data['home_team'],
            data['away_team']
        )
        
        return jsonify({
            'success': True,
            'prediction': pred
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/leagues', methods=['GET'])
def get_leagues():
    """Get available leagues"""
    leagues = [
        {'id': 39, 'name': 'Premier League', 'country': 'England', 'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'},
        {'id': 140, 'name': 'La Liga', 'country': 'Spain', 'flag': '🇪🇸'},
        {'id': 135, 'name': 'Serie A', 'country': 'Italy', 'flag': '🇮🇹'},
        {'id': 78, 'name': 'Bundesliga', 'country': 'Germany', 'flag': '🇩🇪'},
        {'id': 61, 'name': 'Ligue 1', 'country': 'France', 'flag': '🇫🇷'},
        {'id': 2, 'name': 'Champions League', 'country': 'Europe', 'flag': '⚽'},
    ]
    
    return jsonify({
        'success': True,
        'leagues': leagues
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n🚀 Football Predictor API running on http://localhost:{port}")
    print(f"📊 Access predictions at: http://localhost:{port}/predictions\n")
    app.run(host='0.0.0.0', port=port, debug=True)
