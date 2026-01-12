# Feedback Visualizer - Premium Card Edition

Convert Excel feedback rows into premium, social-media-ready image cards with intelligent column detection and letter avatars.

## ✨ Premium Features

- 🧠 **Intelligent Column Detection** - Automatically identifies feedback and author columns (no manual configuration!)
- 🎨 **Premium Card Design** - Rounded corners, gradient backgrounds, professional typography
- 👤 **Letter Avatars** - Circular avatars with pastel colors and initials
- 🌐 **RTL/LTR Support** - Adaptive layout for Arabic and English text
- 📱 **Social Media Ready** - 1080px width, optimized for Instagram, Twitter, Facebook

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Excel File

**No specific column names required!** The script automatically detects:

- **Feedback column** - The column with longest average text
- **Author column** - The column with short text (< 30 chars)

Example Excel structure:
| Name | Comment | ID |
|------|---------|-----|
| محمد أحمد | مرحبا بكم... | 1 |
| Sarah Johnson | Great service! | 2 |

The script will automatically:

- Detect "Comment" as feedback (longest text)
- Detect "Name" as author (short text)
- Ignore "ID" (numeric column)

### 3. Run the Script

```bash
python generate_feedback_images.py
```

### 4. Check Results

```
============================================================
INTELLIGENT COLUMN DETECTION
============================================================
[OK] Found 2 string columns: Name, Comment
  - 'Name': avg length = 15.2 chars
  - 'Comment': avg length = 116.0 chars

[OK] Detected FEEDBACK column: 'Comment' (116.0 chars avg)
[OK] Detected AUTHOR column: 'Name' (15.2 chars avg)
============================================================
```

Cards will be generated in `output_cards/` as `feedback_card_1.png`, `feedback_card_2.png`, etc.

## 📁 Project Structure

```
feedback-visualizer/
├── generate_feedback_images.py   # Main script (Premium Edition)
├── requirements.txt               # Python dependencies
├── feedback_data.xlsx            # Sample input file
├── output_cards/                 # Generated premium cards
│   ├── feedback_card_1.png
│   ├── feedback_card_2.png
│   └── ...
└── README.md                     # This file
```

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **pandas** - Excel file reading and data analysis
- **openpyxl** - Excel engine for pandas
- **Pillow (PIL)** - Image generation, drawing, and manipulation
- **arabic-reshaper** - Arabic character shaping (connects letters)
- **python-bidi** - Bidirectional text algorithm (RTL support)

## 🎨 Premium Design Features

### Card Layout

```
┌─────────────────────────────────────────┐
│  Light Grey Background (#F5F5F5)        │
│  ┌───────────────────────────────────┐ │
│  │  White Card (Rounded Corners)     │ │
│  │  ┌───┐                            │ │
│  │  │ A │  Author Name (Bold)        │ │
│  │  └───┘                            │ │
│  │                                   │ │
│  │  Feedback text here...            │ │
│  │  (Regular font, wrapped)          │ │
│  │                                   │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Letter Avatars

- 🔵 8 pastel colors (blue, green, pink, lavender, peach, yellow)
- ⚪ White letter centered in circle
- 🎯 Automatic first letter extraction
- 🌐 Arabic letter support

### RTL/LTR Adaptive Layout

**Arabic (RTL):**

- Avatar on right side
- Name to left of avatar
- Text right-aligned

**English (LTR):**

- Avatar on left side
- Name to right of avatar
- Text left-aligned

## ⚙️ Configuration Options

Edit the top of `generate_feedback_images.py`:

```python
# Fonts
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Bold for names
FONT_REGULAR_PATH = "C:/Windows/Fonts/arial.ttf"  # Regular for feedback
FONT_SIZE_AUTHOR = 36
FONT_SIZE_FEEDBACK = 42

# File Paths
INPUT_EXCEL = "feedback_data.xlsx"
OUTPUT_DIR = "output_cards"

# Card Design
IMAGE_WIDTH = 1080
CARD_MARGIN = 40
CARD_PADDING = 60
CARD_RADIUS = 30

# Avatar
AVATAR_SIZE = 80
AVATAR_NAME_SPACING = 20
```

## 🔧 How It Works

### 1. Intelligent Column Detection

```python
def detect_columns(df):
    # 1. Filter to string columns only (exclude dates, IDs, numbers)
    # 2. Calculate average character count per column
    # 3. Feedback = column with highest average
    # 4. Author = column with short average (< 30 chars)
```

### 2. Letter Avatar Generation

```python
def generate_avatar(letter, size=80):
    # 1. Create circular transparent image
    # 2. Choose random pastel color
    # 3. Draw circle with color
    # 4. Extract first letter (uppercase)
    # 5. Center white letter in circle
```

### 3. Premium Card Generation

```python
def generate_premium_card(feedback_text, author_name, ...):
    # 1. Process Arabic text (reshape + bidi)
    # 2. Detect RTL/LTR
    # 3. Create image with gradient background
    # 4. Draw rounded rectangle card
    # 5. Generate and position avatar
    # 6. Add author name (bold)
    # 7. Wrap and add feedback text (regular)
    # 8. Save as high-quality PNG
```

## 📝 Example Output

The script generates professional cards like these:

- **Arabic cards** - RTL layout with Arabic text properly rendered
- **English cards** - LTR layout with clean typography
- **Mixed content** - Handles both languages seamlessly

Each card includes:

- Unique letter avatar with pastel color
- Author name in bold
- Feedback text with proper wrapping
- Professional spacing and margins

## 🔧 Troubleshooting

**Font not found error?**

- Update `FONT_BOLD_PATH` and `FONT_REGULAR_PATH` to valid font paths
- Common Windows fonts: `arial.ttf`, `arialbd.ttf`, `tahoma.ttf`

**Column detection incorrect?**

- Check console output to see detected columns
- Ensure your Excel has at least one text column with feedback
- Author column is optional (defaults to "Anonymous")

**Empty cards?**

- Check that your Excel cells contain text
- Empty rows are automatically skipped

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👤 Author

أنا **مصطفى عبد النعيم** — مؤسس **Code Journey**.  
أعمل على **تمكين الشباب من دخول عالم البرمجة بخطوات عملية وواضحة**، من خلال محتوى، تدريب، وتوجيه مبني على التجربة الفعلية.

## 🧭 Code Journey

> تمكين الشباب من دخول عالم البرمجة بخطوات عملية وواضحة.

في **Code Journey**، نؤمن أن التعلم الفعلي يبدأ لما تكتب كود بنفسك.  
هدفنا إننا نساعدك تبدأ رحلتك البرمجية بخطة منظمة، تطبيق واقعي، ودعم حقيقي من مجتمع بيساعد بعض.

## 📬 تقدر تتواصل معايا شخصيًا:

- 💬 واتساب: [اضغط هنا](https://wa.me/201114938410)
- 📧 الإيميل: [mnaeam10@gmail.com](mailto:mnaeam10@gmail.com)  
- 🌐 [الموقع الرسمي](https://mostafa-naeam.vercel.app/)  
- 💼 [LinkedIn](https://www.linkedin.com/in/mostafa-naeam/)

## 💬 تواصل معنا

- 💬 واتساب: [اضغط هنا](https://wa.me/201555303227)
- 📩 البريد الرسمي: [codejourney02@gmail.com](mailto:codejourney02@gmail.com)  
- 💼 [LinkedIn – Code Journey](https://www.linkedin.com/company/code-journey25/)  
- 🌐 [Website – mostafa-naeam](https://mostafa-naeam.vercel.app/)

_Built with ❤️ for premium feedback visualization_