"""
Football Match Predictor - Enhanced with Injury Factors
Uses rule-based system + injury consideration
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
import random


class FootballPredictor:
    """Enhanced football match prediction engine with injury factors"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key or "YOUR_API_KEY_HERE"
        }
        
        # Simulated injury data (in real app, fetch from API)
        self.injuries = {
            'Manchester United': ['Casemiro', 'Lisandro Martinez'],  # 2 key players out
            'Liverpool': [],  # No major injuries
            'Manchester City': ['Kevin De Bruyne'],  # 1 key player out
            'Arsenal': [],
            'Real Madrid': [],
            'Barcelona': ['Pedri'],
            'Inter Milan': [],
            'Juventus': ['Paul Pogba'],
            'Bayern Munich': [],
            'Borussia Dortmund': ['Marco Reus'],
        }
        
    def get_upcoming_matches(self, league_id: int = 39, next_days: int = 7) -> List[Dict]:
        """
        Fetch upcoming matches
        league_id: 39 = Premier League, 140 = La Liga, 135 = Serie A, 78 = Bundesliga
        """
        endpoint = f"{self.base_url}/fixtures"
        
        today = datetime.now()
        from_date = today.strftime("%Y-%m-%d")
        to_date = (today + timedelta(days=next_days)).strftime("%Y-%m-%d")
        
        params = {
            'league': league_id,
            'season': 2025,
            'from': from_date,
            'to': to_date
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"API Error: {response.status_code}")
                return self._get_mock_matches()
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return self._get_mock_matches()
    
    def _get_mock_matches(self) -> List[Dict]:
        """Enhanced mock data with Champions League and World Cup matches"""
        base_time = datetime.now() + timedelta(days=1)
        
        return [
            # Premier League
            {
                'fixture': {
                    'id': 1,
                    'date': base_time.replace(hour=15, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Old Trafford'}
                },
                'teams': {
                    'home': {'id': 33, 'name': 'Manchester United', 'logo': ''},
                    'away': {'id': 40, 'name': 'Liverpool', 'logo': ''}
                },
                'league': {'name': 'Premier League', 'country': 'England', 'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'}
            },
            {
                'fixture': {
                    'id': 2,
                    'date': base_time.replace(hour=17, minute=30, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Etihad Stadium'}
                },
                'teams': {
                    'home': {'id': 50, 'name': 'Manchester City', 'logo': ''},
                    'away': {'id': 42, 'name': 'Arsenal', 'logo': ''}
                },
                'league': {'name': 'Premier League', 'country': 'England', 'flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'}
            },
            
            # Champions League - Tuesday/Wednesday
            {
                'fixture': {
                    'id': 9,
                    'date': (base_time + timedelta(days=2)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Santiago Bernabéu'}
                },
                'teams': {
                    'home': {'id': 541, 'name': 'Real Madrid', 'logo': ''},
                    'away': {'id': 157, 'name': 'Bayern Munich', 'logo': ''}
                },
                'league': {'name': 'Champions League', 'country': 'Europe', 'flag': '⚽'}
            },
            {
                'fixture': {
                    'id': 10,
                    'date': (base_time + timedelta(days=2)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Etihad Stadium'}
                },
                'teams': {
                    'home': {'id': 50, 'name': 'Manchester City', 'logo': ''},
                    'away': {'id': 505, 'name': 'Inter Milan', 'logo': ''}
                },
                'league': {'name': 'Champions League', 'country': 'Europe', 'flag': '⚽'}
            },
            {
                'fixture': {
                    'id': 11,
                    'date': (base_time + timedelta(days=3)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Camp Nou'}
                },
                'teams': {
                    'home': {'id': 529, 'name': 'Barcelona', 'logo': ''},
                    'away': {'id': 212, 'name': 'Paris Saint-Germain', 'logo': ''}
                },
                'league': {'name': 'Champions League', 'country': 'Europe', 'flag': '⚽'}
            },
            
            # La Liga
            {
                'fixture': {
                    'id': 3,
                    'date': (base_time + timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Santiago Bernabéu'}
                },
                'teams': {
                    'home': {'id': 541, 'name': 'Real Madrid', 'logo': ''},
                    'away': {'id': 529, 'name': 'Barcelona', 'logo': ''}
                },
                'league': {'name': 'La Liga', 'country': 'Spain', 'flag': '🇪🇸'}
            },
            
            # Serie A
            {
                'fixture': {
                    'id': 5,
                    'date': (base_time + timedelta(days=2)).replace(hour=19, minute=45, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'San Siro'}
                },
                'teams': {
                    'home': {'id': 505, 'name': 'Inter Milan', 'logo': ''},
                    'away': {'id': 496, 'name': 'Juventus', 'logo': ''}
                },
                'league': {'name': 'Serie A', 'country': 'Italy', 'flag': '🇮🇹'}
            },
            
            # Bundesliga
            {
                'fixture': {
                    'id': 7,
                    'date': (base_time + timedelta(days=3)).replace(hour=17, minute=30, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Allianz Arena'}
                },
                'teams': {
                    'home': {'id': 157, 'name': 'Bayern Munich', 'logo': ''},
                    'away': {'id': 165, 'name': 'Borussia Dortmund', 'logo': ''}
                },
                'league': {'name': 'Bundesliga', 'country': 'Germany', 'flag': '🇩🇪'}
            },
            
            # World Cup 2026 Qualifiers (starting to happen now!)
            {
                'fixture': {
                    'id': 12,
                    'date': (base_time + timedelta(days=4)).replace(hour=19, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Wembley Stadium'}
                },
                'teams': {
                    'home': {'id': 10, 'name': 'England', 'logo': ''},
                    'away': {'id': 768, 'name': 'Italy', 'logo': ''}
                },
                'league': {'name': 'World Cup 2026 Qualifiers', 'country': 'International', 'flag': '🏆'}
            },
            {
                'fixture': {
                    'id': 13,
                    'date': (base_time + timedelta(days=4)).replace(hour=21, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Maracanã'}
                },
                'teams': {
                    'home': {'id': 6, 'name': 'Brazil', 'logo': ''},
                    'away': {'id': 26, 'name': 'Argentina', 'logo': ''}
                },
                'league': {'name': 'World Cup 2026 Qualifiers', 'country': 'International', 'flag': '🏆'}
            },
            {
                'fixture': {
                    'id': 14,
                    'date': (base_time + timedelta(days=5)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat(),
                    'venue': {'name': 'Stade de France'}
                },
                'teams': {
                    'home': {'id': 2, 'name': 'France', 'logo': ''},
                    'away': {'id': 25, 'name': 'Germany', 'logo': ''}
                },
                'league': {'name': 'World Cup 2026 Qualifiers', 'country': 'International', 'flag': '🏆'}
            },
        ]
    
    def predict_match(self, home_team: str, away_team: str, 
                     home_team_id: int = None, away_team_id: int = None) -> Dict:
        """
        Predict match outcome using enhanced AI with injury consideration
        """
        
        # Team strength ratings - Top leagues + International
        team_strength = {
            # Premier League
            'Manchester City': 95, 'Arsenal': 90, 'Liverpool': 89,
            'Aston Villa': 82, 'Tottenham': 81, 'Manchester United': 80,
            'Chelsea': 79, 'Newcastle United': 78, 'Brighton': 75,
            'West Ham': 74, 'Everton': 70, 'Fulham': 69,
            
            # La Liga
            'Real Madrid': 96, 'Barcelona': 91, 'Atletico Madrid': 87,
            'Real Sociedad': 79, 'Athletic Bilbao': 77, 'Real Betis': 76,
            'Villarreal': 75, 'Valencia': 73, 'Sevilla': 72, 'Girona': 74,
            
            # Serie A
            'Inter Milan': 92, 'AC Milan': 85, 'Juventus': 84,
            'Napoli': 83, 'Roma': 80, 'Lazio': 79, 'Atalanta': 82,
            'Fiorentina': 76, 'Bologna': 74,
            
            # Bundesliga
            'Bayern Munich': 94, 'Bayer Leverkusen': 88, 'RB Leipzig': 84,
            'Borussia Dortmund': 86, 'Union Berlin': 76, 'Eintracht Frankfurt': 75,
            'VfB Stuttgart': 77, 'Wolfsburg': 73, 'Freiburg': 74,
            
            # Ligue 1
            'Paris Saint-Germain': 93, 'Monaco': 80, 'Marseille': 79,
            'Lyon': 77, 'Lille': 78, 'Nice': 76,
            
            # Other Champions League Teams
            'Porto': 81, 'Benfica': 80, 'Sporting CP': 79,
            'Ajax': 78, 'PSV': 80, 'Celtic': 74,
            'Red Bull Salzburg': 76, 'Shakhtar Donetsk': 75,
            
            # World Cup 2026 - National Teams
            'Brazil': 94, 'Argentina': 93, 'France': 92,
            'England': 90, 'Spain': 89, 'Germany': 88,
            'Portugal': 87, 'Belgium': 86, 'Netherlands': 87,
            'Italy': 85, 'Uruguay': 82, 'Colombia': 81,
            'Mexico': 78, 'USA': 80, 'Canada': 76,
            'Japan': 77, 'South Korea': 77, 'Morocco': 79,
            'Croatia': 83, 'Denmark': 80, 'Switzerland': 79,
            'Poland': 78, 'Senegal': 78, 'Nigeria': 76,
            'Egypt': 76, 'Ghana': 75, 'Cameroon': 75,
            'Iran': 74, 'Saudi Arabia': 73, 'Australia': 75,
            'Ecuador': 77, 'Peru': 75, 'Chile': 76,
        }
        
        home_strength = team_strength.get(home_team, 70)
        away_strength = team_strength.get(away_team, 70)
        
        score = 0
        reasons = []
        
        # 1. Team strength difference
        strength_diff = home_strength - away_strength
        score += strength_diff * 0.6
        if strength_diff > 10:
            reasons.append(f"{home_team} significantly stronger (rating {home_strength} vs {away_strength})")
        elif strength_diff < -10:
            reasons.append(f"{away_team} significantly stronger (rating {away_strength} vs {home_strength})")
        
        # 2. Home advantage
        home_advantage = 10
        score += home_advantage
        reasons.append("Home advantage (+10 points)")
        
        # 3. Injury impact (NEW FEATURE!)
        home_injuries = len(self.injuries.get(home_team, []))
        away_injuries = len(self.injuries.get(away_team, []))
        injury_impact = (away_injuries - home_injuries) * 8
        score += injury_impact
        
        if home_injuries > 0:
            reasons.append(f"{home_team} missing {home_injuries} key player(s): {', '.join(self.injuries[home_team][:2])}")
        if away_injuries > 0:
            reasons.append(f"{away_team} missing {away_injuries} key player(s): {', '.join(self.injuries[away_team][:2])}")
        
        # 4. Recent form (simulated with randomness for variety)
        home_form = random.uniform(6, 9) if home_strength > 80 else random.uniform(5, 7)
        away_form = random.uniform(6, 9) if away_strength > 80 else random.uniform(5, 7)
        form_diff = (home_form - away_form) * 4
        score += form_diff
        
        # Convert score to prediction
        if score > 12:
            prediction = "Home Win"
            confidence = min(65 + score * 1.2, 92)
        elif score < -12:
            prediction = "Away Win"
            confidence = min(65 + abs(score) * 1.2, 92)
        else:
            prediction = "Draw"
            confidence = min(45 + (10 - abs(score)) * 2, 65)
        
        # Generate realistic score prediction
        score_pred = self._predict_score(home_strength, away_strength, prediction, home_injuries, away_injuries)
        
        # Calculate probabilities
        if prediction == "Home Win":
            home_prob = confidence
            away_prob = (100 - confidence) * 0.4
            draw_prob = 100 - home_prob - away_prob
        elif prediction == "Away Win":
            away_prob = confidence
            home_prob = (100 - confidence) * 0.4
            draw_prob = 100 - home_prob - away_prob
        else:
            draw_prob = confidence
            home_prob = (100 - confidence) * 0.5
            away_prob = 100 - draw_prob - home_prob
        
        return {
            'prediction': prediction,
            'confidence': round(confidence, 1),
            'reasons': reasons[:3],
            'score_prediction': score_pred,
            'home_win_prob': round(home_prob, 1),
            'draw_prob': round(draw_prob, 1),
            'away_win_prob': round(away_prob, 1)
        }
    
    def _predict_score(self, home_str: int, away_str: int, prediction: str, 
                      home_inj: int, away_inj: int) -> str:
        """Generate realistic score prediction"""
        diff = abs(home_str - away_str)
        
        if prediction == "Draw":
            scores = ["1-1", "2-2", "0-0"]
            return random.choice(scores[:2]) if diff < 10 else "1-1"
        
        elif prediction == "Home Win":
            if diff > 20 or (diff > 10 and away_inj > 1):
                return random.choice(["3-0", "4-1", "3-1"])
            elif diff > 10:
                return random.choice(["2-0", "3-1", "2-1"])
            else:
                return random.choice(["2-1", "1-0", "2-0"])
        
        else:  # Away Win
            if diff > 20 or (diff > 10 and home_inj > 1):
                return random.choice(["0-3", "1-4", "1-3"])
            elif diff > 10:
                return random.choice(["0-2", "1-3", "1-2"])
            else:
                return random.choice(["1-2", "0-1", "0-2"])


def test_predictor():
    """Test with enhanced injury-aware predictions"""
    predictor = FootballPredictor()
    
    print("🔮 Football Match Predictor - Enhanced with Injury Analysis")
    print("📊 Testing Top 4 European Leagues\n")
    print("=" * 70)
    
    matches = predictor.get_upcoming_matches()
    
    current_league = None
    for match in matches:
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        date = match['fixture']['date']
        league_name = match['league']['name']
        league_flag = match['league'].get('flag', '')
        
        if current_league != league_name:
            if current_league is not None:
                print("\n" + "=" * 70)
            current_league = league_name
            print(f"\n{league_flag} {league_name.upper()}")
            print("-" * 70)
        
        print(f"\n⚽ {home_team} vs {away_team}")
        print(f"📅 {datetime.fromisoformat(date).strftime('%a, %b %d • %H:%M')}")
        
        prediction = predictor.predict_match(home_team, away_team)
        
        print(f"\n🎯 Prediction: {prediction['prediction']}")
        print(f"📊 Confidence: {prediction['confidence']}%")
        print(f"⚽ Score: {prediction['score_prediction']}")
        print(f"\n📈 Probabilities:")
        print(f"   Home Win: {prediction['home_win_prob']}%")
        print(f"   Draw: {prediction['draw_prob']}%")
        print(f"   Away Win: {prediction['away_win_prob']}%")
        print(f"\n💡 Key Factors:")
        for i, reason in enumerate(prediction['reasons'], 1):
            print(f"   {i}. {reason}")
    
    print("\n" + "=" * 70)
    print(f"\n✅ Total matches analyzed: {len(matches)}")
    print("🏥 Injury data included in predictions!")
    print("🌍 Leagues: Premier League, La Liga, Serie A, Bundesliga")
    print("\n💡 Tip: Run 'python api.py' to start the API server!")


if __name__ == "__main__":
    test_predictor()
