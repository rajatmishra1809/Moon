# app.py
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- Zodiac Data ---
zodiac_signs_data = {
    "aries": {
        "name": "Aries", "dates": "March 21 - April 19",
        "prediction": "Aries, today is a day of bold beginnings. Embrace challenges with your characteristic courage. New opportunities are on the horizon, so trust your instincts."
    },
    "taurus": {
        "name": "Taurus", "dates": "April 20 - May 20",
        "prediction": "Taurus, focus on stability and comfort today. It's a good time for practical matters and strengthening bonds. Find joy in the simple pleasures of life."
    },
    "gemini": {
        "name": "Gemini", "dates": "May 21 - June 20",
        "prediction": "Gemini, your communication skills are highlighted. Engage in stimulating conversations and express your ideas freely. Adaptability will be your greatest asset."
    },
    "cancer": {
        "name": "Cancer", "dates": "June 21 - July 22",
        "prediction": "Cancer, nurture your emotional well-being today. Connect with loved ones and create a peaceful environment. Intuition will guide you towards comfort and understanding."
    },
    "leo": {
        "name": "Leo", "dates": "July 23 - August 22",
        "prediction": "Leo, shine brightly today! Express your creativity and leadership. You have the power to inspire others, so take center stage with confidence."
    },
    "virgo": {
        "name": "Virgo", "dates": "August 23 - September 22",
        "prediction": "Virgo, attention to detail will serve you well. Organize your thoughts and tasks. Practicality and precision will lead to productive outcomes."
    },
    "libra": {
        "name": "Libra", "dates": "September 23 - October 22",
        "prediction": "Libra, seek balance and harmony in all your interactions. Diplomacy and fairness will open doors. It's a good day for partnerships and collaborations."
    },
    "scorpio": {
        "name": "Scorpio", "dates": "October 23 - November 21",
        "prediction": "Scorpio, delve deep into your passions today. Transformative energy is available, allowing you to uncover hidden truths. Trust your powerful intuition."
    },
    "sagittarius": {
        "name": "Sagittarius", "dates": "November 22 - December 21",
        "prediction": "Sagittarius, explore new horizons today. Your adventurous spirit calls for expansion and learning. Embrace optimism and seek out new experiences."
    },
    "capricorn": {
        "name": "Capricorn", "dates": "December 22 - January 19",
        "prediction": "Capricorn, focus on your ambitions and long-term goals. Discipline and perseverance will lead to success. Build strong foundations for your future endeavors."
    },
    "aquarius": {
        "name": "Aquarius", "dates": "January 20 - February 18",
        "prediction": "Aquarius, embrace your unique perspective today. Innovation and humanitarian efforts are favored. Connect with your community and inspire change."
    },
    "pisces": {
        "name": "Pisces", "dates": "February 19 - March 20",
        "prediction": "Pisces, your creativity and empathy are heightened. Allow your intuition to guide you. It's a good day for artistic pursuits and compassionate connections."
    }
}

# --- Tarot Card Data ---
# Updated with actual Wikimedia Commons image URLs
tarot_cards_data = [
    {"name": "The Fool", "meaning": "Beginnings, innocence, spontaneity, a free spirit.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg"},
    {"name": "The Magician", "meaning": "Power, skill, concentration, action, resourcefulness.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg"},
    {"name": "The High Priestess", "meaning": "Intuition, sacred knowledge, divine feminine, unconscious.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg"},
    {"name": "The Empress", "meaning": "Femininity, beauty, nature, nurturing, abundance.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg"},
    {"name": "The Emperor", "meaning": "Authority, structure, control, father figure.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg"},
    {"name": "The Lovers", "meaning": "Love, relationships, choices, union, values alignment.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_06_Lovers.jpg"},
    {"name": "The Chariot", "meaning": "Control, willpower, victory, assertion, determination.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7b/RWS_Tarot_07_Chariot.jpg"},
    {"name": "Strength", "meaning": "Inner strength, courage, patience, compassion, gentle control.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg"},
    {"name": "The Hermit", "meaning": "Soul-searching, introspection, solitude, guidance.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg"},
    {"name": "Wheel of Fortune", "meaning": "Good luck, karma, life cycles, destiny, a turning point.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/33/RWS_Tarot_10_Wheel_of_Fortune.jpg"},
    {"name": "Justice", "meaning": "Fairness, truth, law, cause and effect, objectivity.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg"},
    {"name": "The Hanged Man", "meaning": "Suspension, surrender, new perspectives, sacrifice.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg"},
    {"name": "Death", "meaning": "Endings, change, transformation, transition, letting go.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg"},
    {"name": "Temperance", "meaning": "Balance, moderation, patience, purpose, harmony.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg"},
    {"name": "The Devil", "meaning": "Bondage, addiction, materialism, shadow self.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5c/RWS_Tarot_15_Devil.jpg"},
    {"name": "The Tower", "meaning": "Sudden upheaval, breakdown, revelation, destruction.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/RWS_Tarot_16_Tower.jpg"},
    {"name": "The Star", "meaning": "Hope, inspiration, spirituality, renewal, serenity.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_17_Star.jpg"},
    {"name": "The Moon", "meaning": "Illusion, fear, anxiety, subconscious, intuition.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/RWS_Tarot_18_Moon.jpg"},
    {"name": "The Sun", "meaning": "Joy, success, celebration, positivity, vitality.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/52/RWS_Tarot_19_Sun.jpg"},
    {"name": "Judgement", "meaning": "Reckoning, awakening, absolution, inner calling.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg"},
    {"name": "The World", "meaning": "Completion, integration, accomplishment, travel.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"}
]


@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/zodiac')
def zodiac():
    """Renders the zodiac prediction page."""
    # Pass zodiac data to the template to display all signs
    return render_template('zodiac.html', zodiac_signs=zodiac_signs_data)

@app.route('/get_zodiac_prediction/<sign_key>')
def get_zodiac_prediction(sign_key):
    """Returns the prediction for a specific zodiac sign."""
    sign_data = zodiac_signs_data.get(sign_key.lower())
    if sign_data:
        return jsonify({"success": True, "prediction": sign_data["prediction"]})
    return jsonify({"success": False, "message": "Zodiac sign not found."}), 404

@app.route('/tarot')
def tarot():
    """Renders the tarot card pulling page."""
    return render_template('tarot.html')

@app.route('/draw_tarot_card')
def draw_tarot_card():
    """Returns a randomly drawn tarot card."""
    drawn_card = random.choice(tarot_cards_data)
    return jsonify(drawn_card)

if __name__ == '__main__':
    app.run(debug=True)
