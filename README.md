# ⚽ Football Match Predictor

An AI-powered football match prediction app built with Python (Flask backend) and Flutter (mobile app).

## 🎯 Features

- ✅ **4 Top European Leagues**: Premier League, La Liga, Serie A, Bundesliga
- ✅ 50+ teams with accurate strength ratings
- ✅ Real-time match predictions with AI engine
- ✅ Confidence scores and probability breakdowns (Home/Draw/Away)
- ✅ Detailed reasoning for each prediction
- ✅ Beautiful, modern UI with league filter
- ✅ Score predictions (e.g., 2-1, 3-0)
- ✅ Works offline with mock data (8 sample matches)
- ✅ Easy to expand to more leagues

## 📱 Screenshots

The app displays:
- Upcoming matches
- Win/Draw/Loss predictions with confidence %
- Score predictions (e.g., 2-1)
- Probability bars for each outcome
- Key factors influencing the prediction

## 🚀 Quick Start

### Part 1: Setup Python Backend (5 minutes)

**Step 1: Install Python packages**
```bash
cd football_predictor
pip install -r requirements.txt --break-system-packages
```

**Step 2: Test the predictor**
```bash
python predictor.py
```

You should see predictions for 3 mock matches!

**Step 3: Start the API server**
```bash
python api.py
```

The API will run on `http://localhost:5000`

### Part 2: Setup Flutter App (10 minutes)

**Step 1: Navigate to Flutter project**
```bash
cd flutter_app
```

**Step 2: Install dependencies**
```bash
flutter pub get
```

**Step 3: Update API URL**

Open `lib/main.dart` and change line 40:

```dart
// If testing on phone, use your PC's local IP
final String apiUrl = 'http://YOUR_PC_IP:5000';  // e.g., http://192.168.1.5:5000
```

**Find your PC IP:**
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig` (look for inet)

**Step 4: Run the app**
```bash
flutter run
```

## 📡 Getting Real Data (Optional)

The app works with mock data out of the box. To get real match data:

**Step 1: Get API Key**
1. Go to https://www.api-football.com/
2. Sign up for free account
3. Get your API key (100 free requests/day)

**Step 2: Add API Key**

Create `.env` file:
```bash
FOOTBALL_API_KEY=your_api_key_here
```

Or edit `api.py` line 13:
```python
API_KEY = 'your_api_key_here'
```

**Step 3: Restart API server**
```bash
python api.py
```

Now you'll get real upcoming matches!

## 🏗️ Project Structure

```
football_predictor/
├── predictor.py          # AI prediction engine
├── api.py                # Flask API server
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
└── flutter_app/
    ├── lib/
    │   └── main.dart    # Flutter app
    ├── pubspec.yaml     # Flutter dependencies
    └── android/         # Android config
```

## 🧠 How the AI Works

The prediction engine uses a **rule-based AI system** that considers:

1. **Team Strength** (0-100 rating)
   - Based on recent performance and league position
   - Top teams like Man City get 95, mid-table teams get 70-75

2. **Home Advantage** (+8 points)
   - Home teams statistically win ~40% more often

3. **Recent Form** (last 5 games)
   - Teams on winning streaks get boosted scores

4. **Head-to-Head History**
   - Historical performance between specific teams

5. **Injuries & Suspensions** (coming soon)
   - Missing key players affect predictions

**Algorithm:**
```
score = (home_strength - away_strength) * 0.5
      + home_advantage (8 points)
      + (home_form - away_form) * 5
      + h2h_advantage

if score > 15:  Home Win (75%+ confidence)
if score < -15: Away Win (75%+ confidence)
else:           Draw (50-70% confidence)
```

## 📊 API Endpoints

### `GET /predictions`
Get all upcoming match predictions

**Query Parameters:**
- `league` (optional): League ID (default: 39 = Premier League)

**Response:**
```json
{
  "success": true,
  "count": 3,
  "predictions": [
    {
      "match_id": 1,
      "home_team": {"name": "Manchester United"},
      "away_team": {"name": "Liverpool"},
      "prediction": "Away Win",
      "confidence": 72.5,
      "score_prediction": "1-2",
      "probabilities": {
        "home": 18.0,
        "draw": 25.0,
        "away": 57.0
      },
      "reasons": [
        "Liverpool significantly stronger overall",
        "Liverpool in better recent form",
        "Liverpool has better H2H record"
      ]
    }
  ]
}
```

### `POST /predict`
Predict a specific match

**Request Body:**
```json
{
  "home_team": "Arsenal",
  "away_team": "Chelsea"
}
```

### `GET /leagues`
Get available leagues

### `GET /health`
Health check

## 🎨 Customization

### Add More Teams

Edit `predictor.py` line 93-102:
```python
team_strength = {
    'Manchester City': 95,
    'Arsenal': 88,
    'Liverpool': 87,
    'Your Team Here': 85,  # Add your teams
}
```

### Change Prediction Algorithm

Edit `predict_match()` function in `predictor.py`

### Modify UI Colors

Edit `main.dart` theme colors:
```dart
theme: ThemeData(
  primarySwatch: Colors.blue,  // Change main color
  scaffoldBackgroundColor: Color(0xFF0A1628),  // Background
)
```

## 🔮 Future Improvements

**Short Term:**
- [ ] Add more leagues (La Liga, Serie A, Bundesliga)
- [ ] Injury/suspension data integration
- [ ] Save predictions history
- [ ] User authentication
- [ ] Push notifications for match predictions

**Medium Term:**
- [ ] Machine Learning model (TensorFlow/scikit-learn)
- [ ] Train on 5+ years of historical data
- [ ] Live score updates
- [ ] Post-match accuracy tracking

**Long Term:**
- [ ] Premium features (early predictions, detailed stats)
- [ ] Social features (share predictions, leaderboards)
- [ ] Betting odds comparison
- [ ] Multi-sport support (basketball, tennis)

## 💰 Monetization Ideas

1. **Freemium Model**
   - Free: Today's predictions only
   - Premium ($5-7/month): 48hr early access, all leagues

2. **Ads**
   - Banner ads in free version
   - Remove ads for premium users

3. **Affiliate Marketing**
   - Partner with sports betting sites (18+ regions only)
   - Earn commission on referrals

4. **API Access**
   - Sell API access to other developers
   - $10-50/month for commercial use

## 🐛 Troubleshooting

**App can't connect to API:**
- Make sure API is running: `python api.py`
- Check phone and PC are on same WiFi
- Update `apiUrl` in `main.dart` to your PC's IP
- Turn off firewall temporarily to test

**No predictions showing:**
- API might be rate limited
- Check API logs in terminal
- Try with mock data first (it's built-in)

**Flutter build errors:**
- Run `flutter clean`
- Run `flutter pub get`
- Make sure Flutter SDK is updated

**Python import errors:**
- Make sure all packages installed: `pip install -r requirements.txt --break-system-packages`
- Use Python 3.8+

## 📝 License

Free to use for personal and educational purposes.

## 🤝 Contributing

Want to improve the predictions? Submit a pull request!

## 📧 Support

Questions? Issues? Open an issue on GitHub or contact support.

---

Built with ❤️ using Python, Flask, and Flutter

**Happy Predicting! ⚽🎯**
