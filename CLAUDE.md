# CLAUDE.md — Anonmaly-Detection Codebase Guide

This file provides AI assistants with everything needed to understand, navigate, and contribute to this repository correctly.

---

## Project Overview

**Anonmaly-Detection** is an early-stage research prototype that combines:
- A **static web frontend** for anonymous tip-off/complaint submission
- Three **ML anomaly detection models** (image x2, video x1) trained on the UCF Crime Dataset

The platform allows users to submit anonymous reports of suspicious activity (with image/video/audio evidence). The backend integration (`submit.php`) is not yet implemented in this repository.

---

## Repository Structure

```
Anonmaly-Detection/
├── README.md                        # Minimal (only project title)
├── CLAUDE.md                        # This file
│
├── Front End Web Pages/             # Static HTML/CSS/JS frontend
│   ├── Landing/                     # Homepage
│   │   ├── Landing.html
│   │   ├── Landing.js
│   │   ├── Landing.css
│   │   └── Pic-1.jpg
│   ├── About us/                    # Platform info page
│   │   ├── About.html
│   │   ├── About.js                 # Uses jQuery (not included — broken)
│   │   └── About.css
│   ├── Form/                        # Anonymous complaint submission form
│   │   ├── Form.html                # Submits to submit.php (missing)
│   │   ├── Form.js                  # Has misplaced Node.js server code (bug)
│   │   └── Form.css
│   ├── Response/                    # Post-submission result pages
│   │   ├── Yes-Response.html/css/js # Verified tip response
│   │   ├── No-Response.html/css     # Rejected tip response
│   │   ├── Green Tick.png
│   │   ├── Red Cross.png
│   │   └── Both.jpg
│   └── Contact/                     # Feedback on prior submissions
│       ├── Contact.html
│       └── Contact.css
│
├── Image Anomaly Detection-1/       # Basic CNN model (65K params)
│   ├── image-anomaly-detection.ipynb
│   ├── saved_model.pb
│   ├── keras_metadata.pb
│   └── fingerprint.pb
│
├── Image Anomaly Detection-2/       # DenseNet121 transfer learning (8M params)
│   ├── image-anomaly-detection-2.ipynb
│   ├── saved_model.pb
│   ├── keras_metadata.pb
│   ├── fingerprint.pb
│   └── Variables/
│
└── Video Anomaly Detection/         # Frame-based video classification
    ├── video-anomaly-detection (1).ipynb
    ├── saved_model.pb
    ├── keras_metadata.pb
    └── variables (1).index
```

---

## Technology Stack

### Frontend
- **Pure HTML5 / CSS3 / Vanilla JavaScript** — no framework
- **Google reCAPTCHA v2** — form bot protection
- **Google Fonts (Poppins)** — typography
- **jQuery** — referenced in `About.js` but not loaded (broken dependency)

### Machine Learning
- **Python 3.7+**
- **TensorFlow / Keras** — model definition, training, inference
- **DenseNet121** — pre-trained ImageNet backbone for transfer learning
- **OpenCV (cv2)** — video frame extraction
- **NumPy / Pandas** — data manipulation
- **Matplotlib / Seaborn** — visualization
- **Scikit-learn** — ROC/AUC metrics, preprocessing

### Dataset
- **UCF Crime Dataset** (sourced from Kaggle)
- 14 classes: Abuse, Arrest, Arson, Assault, Burglary, Explosion, Fighting, Normal, RoadAccidents, Robbery, Shooting, Shoplifting, Stealing, Vandalism
- ~1.26M training images, ~111K test images

---

## ML Model Architectures

### Model 1 — Basic CNN (`Image Anomaly Detection-1/`)
- 3x Conv2D (32 → 64 → 64 filters, ReLU)
- 2x MaxPooling2D
- 3x Dense (64 → 64 → 14 neurons)
- Input: 224x224x3, rescaled to 1/255
- 50 epochs, 500 steps/epoch
- Loss: SparseCategoricalCrossentropy
- **65,290 total parameters** — lightweight but limited capacity

### Model 2 — DenseNet121 Transfer Learning (`Image Anomaly Detection-2/`)
- DenseNet121 base (ImageNet weights, frozen)
- GlobalAveragePooling2D
- Dense layers: 256 → 1024 → 512 → 14
- Dropout: 0.3, 0.5, 0.4
- Input: 64x64x3
- Batch size: 64
- **8,095,054 total parameters** (7.9M trainable)

### Model 3 — Video Frame Classifier (`Video Anomaly Detection/`)
- Same architecture as Model 2 (DenseNet121 + custom classifier)
- Frame-level predictions from extracted video frames
- Learning rate: 0.00003
- ROC/AUC evaluation per class

All models are saved in **TensorFlow SavedModel format** (`.pb` files).

---

## Frontend Conventions

### JavaScript
- **Naming:** camelCase for variables and functions
- **DOM access:** `document.getElementById()`, `document.createElement()`
- **Events:** `element.addEventListener('click', function() { ... })`
- **Init pattern:** `window.onload = function() { ... }`
- No build step — files served directly

### CSS
- **Primary color:** `#ff7200` (orange)
- **Backgrounds:** Dark (`#08071d`, `#333`)
- **Text on dark:** white; text on light: dark
- **Transitions:** 0.3s–0.4s ease
- **Font:** Poppins (Google Fonts)
- Class naming loosely follows BEM (`.form`, `.form-group`, `.submit-button`)
- No preprocessor (no Sass/Less)

### Form Flow
```
Landing.html → Form.html → submit.php [MISSING] → Yes-Response.html or No-Response.html
```

---

## Known Bugs & Issues

> These are existing issues — do not silently work around them without noting the fix.

| Location | Issue |
|---|---|
| `Form/Form.js` lines 46–58 | Node.js HTTP server code inside a browser JS file — non-functional |
| `About us/About.js` | Uses `$(document).ready()` but jQuery is not loaded in About.html |
| `Form/Form.html` | `action="submit.php"` targets a backend file not present in the repo |
| All notebooks | `model.save('')` uses empty string path — model save destination is unclear |
| `Image Anomaly Detection-1/` | Training instability (30–75% accuracy variance across epochs) |
| Repository root | No `.gitignore` — binary model files and temp files committed directly |
| Repository root | No `requirements.txt` — Python dependencies undocumented |

---

## Development Workflow

There is no automated build pipeline. Development is manual:

### Frontend
1. Open HTML files directly in a browser (no server required for basic review)
2. To test form submission, a PHP/Node.js server must handle `submit.php`
3. No bundler, transpiler, or minifier is used

### ML Models
1. Source data from Kaggle: UCF Crime Dataset
2. Open notebooks in Jupyter Lab or Jupyter Notebook
3. Run cells sequentially — each notebook is self-contained
4. Models save to local directory in TensorFlow SavedModel format
5. No automated training scripts exist

### Running Locally (Minimal Setup)
```bash
# Python dependencies (install manually — no requirements.txt exists)
pip install tensorflow opencv-python numpy pandas matplotlib seaborn scikit-learn jupyter

# Start Jupyter
jupyter notebook

# For frontend: open HTML files in browser directly
# Or serve with any static server:
python -m http.server 8080
```

---

## Git Conventions

### Current State
- Commit messages have historically been low-quality (`"Create trash"`, `"Delete trash"`)
- No `.gitignore` — binary files are committed directly
- No conventional commit format enforced

### Recommended Conventions (for new work)
Use conventional commit format:
```
feat: add backend handler for form submission
fix: load jQuery in About.html before About.js
docs: update README with setup instructions
chore: add .gitignore for Python and Jupyter artifacts
```

### Branch
All documentation/AI-assisted changes go on: `claude/add-claude-documentation-T2cVn`

---

## What Is Missing (For Context)

When working on this repo, be aware these components do not yet exist:
- `submit.php` — backend form handler
- `requirements.txt` — Python dependency list
- `.gitignore` — file exclusion rules
- Any server-side validation
- Any test suite (no pytest, no Jest, no integration tests)
- CI/CD pipeline
- Deployment configuration

---

## Security Notes

- The reCAPTCHA **site key** is embedded in `Form.html` source (public client-side key — acceptable by design)
- No HTTPS enforcement is configured
- No server-side input validation is implemented
- Do not add hardcoded secrets, API keys, or credentials to any file

---

## Guidance for AI Assistants

- **Read files before editing** — the codebase has existing bugs; understand context first
- **Do not silently fix existing bugs** unless the task explicitly requests it — document them instead
- **No build step** — HTML/CSS/JS changes are immediately reflected; no compilation needed
- **Notebook changes** — edit `.ipynb` files carefully; cell outputs are stored in JSON and can bloat the file
- **Model files** (`.pb`, `.index`) are binary — do not attempt to edit them as text
- **Backend is absent** — do not assume `submit.php` exists or will be created in any task unless specified
- **No test runner** — there is no command to run tests; validate frontend changes manually in browser
- **Commit scope** — only commit to the branch listed above unless given explicit permission to push elsewhere
