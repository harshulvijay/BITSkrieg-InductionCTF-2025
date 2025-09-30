from flask import Flask, request, jsonify, session, send_from_directory, render_template
import os
from flask_cors import CORS
import uuid
import time
from utils import Mines, GRID_SIZE, MINE_COUNT

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)
FLAG = os.getenv('FLAG', 'InductionCTF{fake_flag}')
active_games = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('public', filename)

def get_user_balance():
    if 'balance' not in session:
        session['balance'] = 1000
    return session['balance']

def update_user_balance(new_balance):
    session['balance'] = new_balance

@app.route("/status", methods=["GET"])
def status():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    if 'balance' not in session:
        session['balance'] = 1000
    
    user_id = session.get('user_id')
    balance = get_user_balance()
    return jsonify({
        "success": True,
        "user_id": user_id,
        "balance": balance
        }), 200

@app.route("/start_game", methods=["POST"])
def start_game():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    data = request.get_json()
    bet_amount = data.get('bet_amount', 100)

    balance = get_user_balance()
    if bet_amount > balance:
        return jsonify({
            'success': False,
            'error': 'Insufficient balance'
        }), 400
    
    new_balance = balance - bet_amount
    update_user_balance(new_balance)

    server_time = int(time.time())
    game = Mines(user_id, bet_amount, server_time)
    game_id = str(uuid.uuid4())
    active_games[game_id] = game

    return jsonify({
        'success': True,
        'server_time': server_time,
        'game_id': game_id,
        'balance': new_balance,
        'bet_amount': bet_amount,
        'grid_size': GRID_SIZE,
        'mine_count': MINE_COUNT
    }), 200

@app.route('/api/reveal-tile', methods=['POST'])
def reveal_tile():
    data = request.get_json()
    game_id = data.get('game_id')
    position = data.get('position')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    if game_id not in active_games:
        return jsonify({
            'success': False,
            'error': 'Game not found'
        }), 404
    
    game = active_games[game_id]
    if game.user_id != user_id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized access to game'
        }), 403
    
    if position < 0 or position >= GRID_SIZE:
        return jsonify({
            'success': False,
            'error': 'Invalid tile position'
        }), 400
    
    success = game.reveal_tile(position)

    response = {
        'success': success,
        'game_id': game_id,
        'position': position,
        'game_over': game.game_over,
        'current_multiplier': round(game.current_multiplier, 2),
        'potential_payout': game.calculate_payout(),
        'safe_tiles_found': game.safe_tiles_found
    }

    if not success and game.game_over:
        response['message'] = 'You hit a mine!'
        response['mines_revealed'] = sorted(game.mines_positions)
    elif success:
        response['message'] = 'Safe tile! Continue or cash out?'
    
    return jsonify(response), 200

@app.route('/api/cash-out', methods=['POST'])
def cash_out():
    data = request.get_json()
    game_id = data.get('game_id')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    if game_id not in active_games:
        return jsonify({
            'success': False,
            'error': 'Game not found'
        }), 404
    
    game = active_games[game_id]
    if game.user_id != user_id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized access to game'
        }), 403
    
    payout = game.cash_out()
    if payout > 0:
        current_balance = get_user_balance()
        new_balance = current_balance + payout
        update_user_balance(new_balance)

        flag_earned = new_balance > 1_000_000
        response = {
            'success': True,
            'payout': payout,
            'new_balance': new_balance,
            'message': f'Congratulations! You won ${payout}!'
        }
        if flag_earned:
            response['flag'] = FLAG
        return jsonify(response), 200
    
    return jsonify({
        'success': False,
        'message': 'No safe tiles found to cash out.'
    }), 400

@app.route('/api/game-state', methods=['GET'])
def game_state():
    game_id = request.args.get('game_id')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    if game_id not in active_games:
        return jsonify({
            'success': False,
            'error': 'Game not found'
        }), 404
    game = active_games[game_id]
    if game.user_id != user_id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized access to game'
        }), 403 
    
    return jsonify({
        'success': True,
        'game_id': game_id,
        'grid_revealed': game.grid_revealed,
        'safe_tiles_found': game.safe_tiles_found,
        'game_over': game.game_over,
        'won': game.won,
        'bet_amount': game.bet_amount,
        'current_multiplier': round(game.current_multiplier, 2),
        'mines_positions': sorted(game.mines_positions) if game.game_over else []
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)









    
