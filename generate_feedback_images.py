"""
Feedback Visualizer - Premium Card Edition
Convert Excel feedback rows to premium social-media-ready image cards
Supports unstructured data with intelligent column detection
Supports Arabic text with proper RTL rendering
"""

import os
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# ============================================================================
# CONFIGURATION - Modify these variables as needed
# ============================================================================

# Font Configuration
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Bold font for author names
FONT_REGULAR_PATH = "C:/Windows/Fonts/arial.ttf"  # Regular font for feedback
FONT_SIZE_AUTHOR = 36  # Font size for author name
FONT_SIZE_FEEDBACK = 42  # Font size for feedback text

# File Paths
INPUT_EXCEL = "feedback_data.xlsx"  # Input Excel file
OUTPUT_DIR = "output_cards"  # Directory for generated images

# Image Dimensions
IMAGE_WIDTH = 1080  # Fixed width (social media standard)
CARD_MARGIN = 40  # Margin around the card
CARD_PADDING = 60  # Padding inside the card
CARD_RADIUS = 30  # Corner radius for rounded rectangle

# Avatar Configuration
AVATAR_SIZE = 80  # Avatar diameter in pixels
AVATAR_NAME_SPACING = 20  # Space between avatar and name

# Styling
BACKGROUND_COLOR = (245, 245, 245)  # Light grey background
CARD_COLOR = (255, 255, 255)  # White card
TEXT_COLOR_AUTHOR = (40, 40, 40)  # Dark grey for author
TEXT_COLOR_FEEDBACK = (60, 60, 60)  # Slightly lighter grey for feedback
LINE_SPACING = 20  # Additional spacing between lines

# Pastel Colors for Avatars
PASTEL_COLORS = [
    (174, 198, 207),  # Pastel Blue
    (189, 224, 254),  # Light Blue
    (162, 210, 223),  # Sky Blue
    (188, 224, 187),  # Pastel Green
    (255, 218, 193),  # Peach
    (255, 204, 229),  # Pink
    (230, 190, 255),  # Lavender
    (255, 255, 186),  # Pale Yellow
]

# ============================================================================
# HELPER FUNCTIONS - Column Detection
# ============================================================================

def detect_columns(df):
    """
    Intelligently detect feedback and author columns using heuristic analysis.
    
    Algorithm:
    1. Filter to string columns only (exclude dates, numbers, IDs)
    2. Calculate average character count per column
    3. Feedback Body = column with highest average character count
    4. Author Name = column with short average length (< 30 chars)
    
    Args:
        df: pandas DataFrame
    
    Returns:
        tuple: (feedback_column_name, author_column_name)
    """
    print("\n" + "=" * 60)
    print("INTELLIGENT COLUMN DETECTION")
    print("=" * 60)
    
    # Filter to string columns only
    string_columns = []
    for col in df.columns:
        # Check if column contains mostly strings
        if df[col].dtype == 'object':
            # Further filter: check if it's actually text (not dates, etc.)
            sample = df[col].dropna().head(5)
            if len(sample) > 0 and all(isinstance(x, str) for x in sample):
                string_columns.append(col)
    
    if len(string_columns) == 0:
        print("[ERROR] No string columns found in Excel file!")
        return None, None
    
    print(f"[OK] Found {len(string_columns)} string columns: {', '.join(string_columns)}")
    
    # Calculate average character count for each string column
    column_stats = {}
    for col in string_columns:
        # Calculate average length, ignoring empty/null values
        lengths = df[col].dropna().apply(lambda x: len(str(x)) if isinstance(x, str) else 0)
        avg_length = lengths.mean() if len(lengths) > 0 else 0
        column_stats[col] = avg_length
        print(f"  - '{col}': avg length = {avg_length:.1f} chars")
    
    # Detect Feedback Body (longest average text)
    feedback_col = max(column_stats, key=column_stats.get)
    print(f"\n[OK] Detected FEEDBACK column: '{feedback_col}' ({column_stats[feedback_col]:.1f} chars avg)")
    
    # Detect Author Name (short text, < 30 chars average)
    author_col = None
    for col, avg_len in sorted(column_stats.items(), key=lambda x: x[1]):
        if col != feedback_col and avg_len < 30 and avg_len > 0:
            author_col = col
            break
    
    if author_col:
        print(f"[OK] Detected AUTHOR column: '{author_col}' ({column_stats[author_col]:.1f} chars avg)")
    else:
        print("[WARNING] Could not detect author column, will use 'Anonymous'")
    
    print("=" * 60 + "\n")
    
    return feedback_col, author_col


# ============================================================================
# HELPER FUNCTIONS - Font Loading
# ============================================================================

def load_font(font_path, size):
    """
    Load a TrueType font with fallback to default if not found.
    
    Args:
        font_path: Path to the .ttf font file
        size: Font size in pixels
    
    Returns:
        ImageFont object
    """
    try:
        font = ImageFont.truetype(font_path, size)
        return font
    except Exception as e:
        print(f"[WARNING] Could not load font '{font_path}': {e}")
        print(f"[WARNING] Falling back to default font")
        return ImageFont.load_default()


# ============================================================================
# HELPER FUNCTIONS - Arabic Text Processing
# ============================================================================

def process_arabic_text(text):
    """
    Process Arabic text for proper RTL rendering.
    
    This function:
    1. Reshapes Arabic characters to connect them properly
    2. Applies bidirectional algorithm for RTL display
    
    Args:
        text: Input text (may contain Arabic)
    
    Returns:
        Properly formatted text for rendering
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Reshape Arabic characters (connects letters properly)
    reshaped_text = reshape(text)
    
    # Apply bidirectional algorithm (handles RTL direction)
    bidi_text = get_display(reshaped_text)
    
    return bidi_text


def is_arabic(text):
    """
    Detect if text contains Arabic characters.
    
    Args:
        text: Input text
    
    Returns:
        bool: True if text contains Arabic characters
    """
    if not text:
        return False
    
    # Check for Arabic Unicode range (0600-06FF)
    for char in str(text):
        if '\u0600' <= char <= '\u06FF':
            return True
    return False


# ============================================================================
# HELPER FUNCTIONS - Avatar Generation
# ============================================================================

def generate_avatar(letter, size=80):
    """
    Generate a circular letter avatar with pastel background.
    
    Args:
        letter: First letter of the name
        size: Diameter of the avatar in pixels
    
    Returns:
        PIL Image object (RGBA mode for transparency)
    """
    # Create transparent image
    avatar = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(avatar)
    
    # Choose random pastel color
    bg_color = random.choice(PASTEL_COLORS)
    
    # Draw circle
    draw.ellipse([0, 0, size, size], fill=bg_color)
    
    # Load font for letter (use bold font, larger size)
    letter_font_size = int(size * 0.5)  # Letter is 50% of avatar size
    letter_font = load_font(FONT_BOLD_PATH, letter_font_size)
    
    # Get the first letter (uppercase)
    letter = str(letter)[0].upper() if letter else "?"
    
    # Process Arabic letter if needed
    if is_arabic(letter):
        letter = process_arabic_text(letter)
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), letter, font=letter_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]
    
    # Draw letter in white
    draw.text((x, y), letter, font=letter_font, fill=(255, 255, 255, 255))
    
    return avatar


# ============================================================================
# HELPER FUNCTIONS - Text Wrapping
# ============================================================================

def wrap_text(text, font, max_width):
    """
    Wrap text into multiple lines to fit within max_width.
    
    Algorithm:
    1. Split text into words
    2. Build lines by adding words until width exceeds max_width
    3. When a line is full, start a new line
    4. Handle edge case: if a single word is too long, force it on its own line
    
    Args:
        text: Text to wrap
        font: ImageFont object for measuring text width
        max_width: Maximum width in pixels
    
    Returns:
        List of text lines
    """
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Test if adding this word would exceed max width
        test_line = f"{current_line} {word}".strip()
        
        # Get bounding box to measure text width
        bbox = font.getbbox(test_line)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            # Word fits, add it to current line
            current_line = test_line
        else:
            # Word doesn't fit
            if current_line:
                # Save current line and start new one with this word
                lines.append(current_line)
                current_line = word
            else:
                # Edge case: single word is too long, force it anyway
                lines.append(word)
                current_line = ""
    
    # Don't forget the last line
    if current_line:
        lines.append(current_line)
    
    return lines


# ============================================================================
# HELPER FUNCTIONS - Drawing
# ============================================================================

def draw_rounded_rectangle(draw, xy, radius, fill):
    """
    Draw a rounded rectangle.
    
    Args:
        draw: ImageDraw object
        xy: Tuple of (x1, y1, x2, y2) coordinates
        radius: Corner radius
        fill: Fill color
    """
    x1, y1, x2, y2 = xy
    
    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # Draw four corners
    draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)


# ============================================================================
# MAIN IMAGE GENERATION
# ============================================================================

def generate_premium_card(feedback_text, author_name, output_path, font_bold, font_regular):
    """
    Generate a premium card image with avatar, author name, and feedback text.
    
    Args:
        feedback_text: Feedback text to render
        author_name: Author's name
        output_path: Path to save the image
        font_bold: Bold font for author name
        font_regular: Regular font for feedback text
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Process text for Arabic support
        processed_feedback = process_arabic_text(feedback_text)
        processed_author = process_arabic_text(author_name) if author_name else "Anonymous"
        
        # Detect if text is RTL (Arabic)
        is_rtl = is_arabic(feedback_text) or is_arabic(author_name)
        
        # Calculate card dimensions
        card_width = IMAGE_WIDTH - (CARD_MARGIN * 2)
        card_x1 = CARD_MARGIN
        card_x2 = IMAGE_WIDTH - CARD_MARGIN
        
        # Calculate available width for text
        max_text_width = card_width - (CARD_PADDING * 2)
        
        # Wrap feedback text
        feedback_lines = wrap_text(processed_feedback, font_regular, max_text_width)
        
        # Calculate heights
        author_bbox = font_bold.getbbox(processed_author)
        author_height = author_bbox[3] - author_bbox[1]
        
        feedback_bbox = font_regular.getbbox("Ay")
        feedback_line_height = feedback_bbox[3] - feedback_bbox[1]
        
        # Header height (avatar or author name, whichever is taller)
        header_height = max(AVATAR_SIZE, author_height)
        
        # Total feedback text height
        total_feedback_height = (feedback_line_height * len(feedback_lines)) + (LINE_SPACING * (len(feedback_lines) - 1))
        
        # Calculate total card height
        card_content_height = header_height + 40 + total_feedback_height  # 40px spacing between header and feedback
        card_height = card_content_height + (CARD_PADDING * 2)
        
        # Calculate image height
        image_height = card_height + (CARD_MARGIN * 2)
        
        # Create image with background
        image = Image.new('RGB', (IMAGE_WIDTH, image_height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)
        
        # Draw card (rounded rectangle)
        card_y1 = CARD_MARGIN
        card_y2 = image_height - CARD_MARGIN
        draw_rounded_rectangle(draw, (card_x1, card_y1, card_x2, card_y2), CARD_RADIUS, CARD_COLOR)
        
        # Generate and position avatar
        avatar = generate_avatar(author_name if author_name else "A", AVATAR_SIZE)
        
        # Calculate header positions
        current_y = CARD_MARGIN + CARD_PADDING
        
        if is_rtl:
            # RTL: Avatar on right, name to its left
            avatar_x = card_x2 - CARD_PADDING - AVATAR_SIZE
            image.paste(avatar, (avatar_x, current_y), avatar)
            
            # Author name to the left of avatar
            author_bbox = font_bold.getbbox(processed_author)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = avatar_x - AVATAR_NAME_SPACING - author_width
            author_y = current_y + (AVATAR_SIZE - author_height) // 2  # Vertically center with avatar
            draw.text((author_x, author_y), processed_author, font=font_bold, fill=TEXT_COLOR_AUTHOR)
        else:
            # LTR: Avatar on left, name to its right
            avatar_x = card_x1 + CARD_PADDING
            image.paste(avatar, (avatar_x, current_y), avatar)
            
            # Author name to the right of avatar
            author_x = avatar_x + AVATAR_SIZE + AVATAR_NAME_SPACING
            author_y = current_y + (AVATAR_SIZE - author_height) // 2  # Vertically center with avatar
            draw.text((author_x, author_y), processed_author, font=font_bold, fill=TEXT_COLOR_AUTHOR)
        
        # Move to feedback text position
        current_y += header_height + 40  # 40px spacing
        
        # Draw feedback text
        for line in feedback_lines:
            # Get text width for alignment
            bbox = font_regular.getbbox(line)
            text_width = bbox[2] - bbox[0]
            
            if is_rtl:
                # Right-aligned for RTL
                text_x = card_x2 - CARD_PADDING - text_width
            else:
                # Left-aligned for LTR
                text_x = card_x1 + CARD_PADDING
            
            draw.text((text_x, current_y), line, font=font_regular, fill=TEXT_COLOR_FEEDBACK)
            current_y += feedback_line_height + LINE_SPACING
        
        # Save image
        image.save(output_path, 'PNG', quality=95)
        return True
        
    except Exception as e:
        print(f"[ERROR] Error generating card: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to process Excel file and generate premium cards.
    """
    print("=" * 60)
    print("Feedback Visualizer - Premium Card Edition")
    print("=" * 60)
    
    # Load fonts
    font_bold = load_font(FONT_BOLD_PATH, FONT_SIZE_AUTHOR)
    font_regular = load_font(FONT_REGULAR_PATH, FONT_SIZE_FEEDBACK)
    print(f"[OK] Fonts loaded")
    
    # Check if input file exists
    if not os.path.exists(INPUT_EXCEL):
        print(f"\n[ERROR] Input file '{INPUT_EXCEL}' not found!")
        print(f"  Please create the Excel file or update INPUT_EXCEL path.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[OK] Output directory: {OUTPUT_DIR}")
    
    # Read Excel file
    try:
        df = pd.read_excel(INPUT_EXCEL)
        print(f"[OK] Loaded Excel file: {INPUT_EXCEL}")
        print(f"  Total rows: {len(df)}")
        print(f"  Columns: {', '.join(df.columns)}")
    except Exception as e:
        print(f"\n[ERROR] Error reading Excel file: {e}")
        return
    
    # Intelligent column detection
    feedback_col, author_col = detect_columns(df)
    
    if not feedback_col:
        print("[ERROR] Could not detect feedback column!")
        return
    
    print("-" * 60)
    print("Generating premium cards...")
    print("-" * 60)
    
    # Process each row
    success_count = 0
    skip_count = 0
    
    for index, row in df.iterrows():
        feedback_text = row[feedback_col]
        author_name = row[author_col] if author_col and author_col in row else "Anonymous"
        
        # Skip empty rows
        if pd.isna(feedback_text) or str(feedback_text).strip() == "":
            skip_count += 1
            print(f"[SKIP] Row {index + 1}: Skipped (empty feedback)")
            continue
        
        # Handle missing author name
        if pd.isna(author_name) or str(author_name).strip() == "":
            author_name = "Anonymous"
        
        # Generate output filename (1-indexed to match row numbers)
        output_filename = f"feedback_card_{index + 1}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Generate card
        if generate_premium_card(str(feedback_text), str(author_name), output_path, font_bold, font_regular):
            success_count += 1
            print(f"[OK] Row {index + 1}: Generated {output_filename}")
        else:
            print(f"[ERROR] Row {index + 1}: Failed to generate {output_filename}")
    
    # Summary
    print("-" * 60)
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total rows processed: {len(df)}")
    print(f"Cards generated: {success_count}")
    print(f"Rows skipped (empty): {skip_count}")
    print(f"Output location: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
