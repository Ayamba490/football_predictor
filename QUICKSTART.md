# ⚡ QUICKSTART GUIDE - Football Match Predictor

## 🎯 What You're Getting

A complete AI-powered football prediction app:
- **Python Backend**: Predicts match outcomes using AI
- **Flutter Mobile App**: Beautiful UI to view predictions
- **Works Offline**: Built-in mock data for testing

## 📦 What's Included

```
football_predictor/
├── predictor.py           ← AI prediction engine
├── api.py                 ← API server
├── requirements.txt       ← Python packages
├── setup.bat             ← Windows setup script
├── README.md             ← Full documentation
│
└── flutter_app/
    ├── lib/main.dart     ← Mobile app
    └── pubspec.yaml      ← Flutter config
```

## 🚀 Get Started in 3 Steps

### Step 1: Setup Backend (2 minutes)

```bash
# Extract the files
# Open terminal in football_predictor folder

# Install Python packages
pip install -r requirements.txt --break-system-packages

# Test it works
python predictor.py
```

You'll see predictions like:
```
⚽ Manchester United vs Liverpool
🎯 Prediction: Away Win
📊 Confidence: 72.5%
⚽ Score: 1-2
```

### Step 2: Start API Server

```bash
python api.py
```

Server runs at: `http://localhost:5000`

### Step 3: Run Mobile App

```bash
cd flutter_app
flutter pub get
flutter run
```

**IMPORTANT:** Before running, edit `lib/main.dart` line 40:
```dart
final String apiUrl = 'http://YOUR_PC_IP:5000';
```

Find your PC IP:
- Windows: `ipconfig` 
- Look for "IPv4 Address" like `192.168.1.5`

## 📱 What The App Looks Like

```
┌─────────────────────────────────────┐
│  ⚽ Match Predictions           🔄  │
├─────────────────────────────────────┤
│                                     │
│  Premier League • Sat, Feb 15      │
│  ┌─────────────────────────────┐   │
│  │    Man Utd     VS   Liverpool│   │
│  │       🛡️             🛡️       │   │
│  │                1-2            │   │
│  │                               │   │
│  │  🎯 PREDICTION: Away Win     │   │
│  │  Confidence: 72.5%           │   │
│  │                               │   │
│  │  Home: ▓▓░░░ 18%             │   │
│  │  Draw: ▓▓▓░░ 25%             │   │
│  │  Away: ▓▓▓▓▓ 57%             │   │
│  │                               │   │
│  │  💡 Key Factors:             │   │
│  │  • Liverpool stronger         │   │
│  │  • Better recent form         │   │
│  │  • Wins H2H historically      │   │
│  └─────────────────────────────┘   │
│                                     │
│  [More matches...]                  │
│                                     │
└─────────────────────────────────────┘
```

## 🧪 Test It First

**Without API (Mock Data):**
The app works immediately with 3 sample matches built-in!

**With Real API (Optional):**
1. Get free API key: https://www.api-football.com/
2. Add to `.env` file or `api.py`
3. Restart server

## ⚙️ Customize It

**Add Your Favorite Team:**
Edit `predictor.py` line 93:
```python
team_strength = {
    'Manchester City': 95,
    'Your Team': 85,  # Add here
}
```

**Change Colors:**
Edit `main.dart` theme:
```dart
primarySwatch: Colors.blue,  // Main color
```

**Different League:**
In `api.py`, change:
```python
league_id = 140  # La Liga
league_id = 135  # Serie A
league_id = 78   # Bundesliga
```

## 🐛 Common Issues

**"Can't connect to API"**
→ Make sure `python api.py` is running
→ Update `apiUrl` in main.dart to your PC's IP
→ Phone and PC must be on same WiFi

**"Module not found"**
→ Run: `pip install -r requirements.txt --break-system-packages`

**"No predictions"**
→ The app has mock data built-in, should always work
→ Check API terminal for errors

## 💡 Pro Tips

1. **Start with mock data** - Don't worry about API keys initially
2. **Test predictions accuracy** - Track results over time
3. **Improve algorithm** - Edit `predict_match()` function
4. **Add more features** - See TODO list in README

## 📈 Next Steps

Once it works:
1. ✅ Track prediction accuracy over 10-20 matches
2. ✅ Post predictions on Twitter/Reddit
3. ✅ Build credibility (aim for 70%+ accuracy)
4. ✅ Add premium features
5. ✅ Launch on App Store / Play Store

## 🎯 Goal

Build this into a real business:
- Free tier with ads
- Premium: $5-7/month
- Target: 1000 users = $5k-7k/month

## 💪 You Got This!

Everything is ready to go. Just follow the steps above and you'll have a working prediction app in 10 minutes!

Questions? Check the full README.md for detailed docs.

**Good luck! ⚽🚀**
