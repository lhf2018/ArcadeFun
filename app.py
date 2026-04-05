# app.py - 主应用程序文件
from flask import Flask, render_template, request, jsonify, session
import random
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'arcadefun_secret_key_2026'

# 游戏配置
GAMES_CONFIG = {
    'slots': {'name': '老虎机', 'icon': '🎰', 'cost': 5, 'leverage': True},
    'wheel': {'name': '幸运轮盘', 'icon': '🎡', 'cost': 3, 'leverage': True},
    'balloons': {'name': '打气球', 'icon': '🎈', 'cost': 2, 'leverage': False},
    'chest': {'name': '神秘宝箱', 'icon': '🎁', 'cost': 10, 'leverage': True},
    'updown': {'name': '涨跌猜', 'icon': '📈', 'cost': 5, 'leverage': True},
    'gacha': {'name': '扭蛋机', 'icon': '🥚', 'cost': 15, 'leverage': False},
    'scratch': {'name': '刮刮乐', 'icon': '🎫', 'cost': 5, 'leverage': True},
    'lottery': {'name': '体育彩票', 'icon': '🏀', 'cost': 10, 'leverage': True}
}

# 老虎机符号
SLOTS_SYMBOLS = ['🎰', '7️⃣', '💎', '💰', '⭐', '🔔', '🃏', '🎲', '🍒', '🍋', '🍊', '🍉', '🍇', '💵']
SLOTS_PAYOUT = {
    ('🎰', '🎰', '🎰'): 500,
    ('7️⃣', '7️⃣', '7️⃣'): 300,
    ('💎', '💎', '💎'): 200,
    ('💰', '💰', '💰'): 150,
    ('⭐', '⭐', '⭐'): 100,
    ('🔔', '🔔', '🔔'): 80,
    ('🃏', '🃏', '🃏'): 70,
    ('🎲', '🎲', '🎲'): 60,
}

FRUIT_SYMBOLS = ['🍒', '🍋', '🍊', '🍉', '🍇']
HIGH_VALUE_SYMBOLS = ['🎰', '7️⃣', '💎', '💰']

# 轮盘配置
WHEEL_SECTORS = [
    {'value': 200, 'color': '#FFD700', 'label': '200'},
    {'value': 100, 'color': '#FF4444', 'label': '100'},
    {'value': 50, 'color': '#FF8C00', 'label': '50'},
    {'value': 20, 'color': '#FFD700', 'label': '20'},
    {'value': 10, 'color': '#32CD32', 'label': '10'},
    {'value': 5, 'color': '#4169E1', 'label': '5'},
    {'value': 0, 'color': '#808080', 'label': '0'},
    {'value': 50, 'color': '#FF8C00', 'label': '50'},
    {'value': 20, 'color': '#FFD700', 'label': '20'},
    {'value': 10, 'color': '#32CD32', 'label': '10'},
    {'value': 5, 'color': '#4169E1', 'label': '5'},
    {'value': 0, 'color': '#808080', 'label': '0'}
]

# 宝箱奖励概率
CHEST_REWARDS = [
    (0, 5), (5, 10), (10, 20), (15, 20), (20, 15),
    (30, 10), (50, 10), (100, 7), (200, 2), (500, 1)
]

# 扭蛋图鉴
GACHA_ITEMS = [
    {'id': 1, 'name': '小熊', 'icon': '🧸', 'rarity': '普通', 'probability': 15},
    {'id': 2, 'name': '小猫', 'icon': '🐱', 'rarity': '普通', 'probability': 15},
    {'id': 3, 'name': '小狗', 'icon': '🐶', 'rarity': '普通', 'probability': 15},
    {'id': 4, 'name': '兔子', 'icon': '🐰', 'rarity': '普通', 'probability': 15},
    {'id': 5, 'name': '企鹅', 'icon': '🐧', 'rarity': '稀有', 'probability': 10},
    {'id': 6, 'name': '独角兽', 'icon': '🦄', 'rarity': '稀有', 'probability': 8},
    {'id': 7, 'name': '小龙', 'icon': '🐉', 'rarity': '稀有', 'probability': 7},
    {'id': 8, 'name': '机器人', 'icon': '🤖', 'rarity': '稀有', 'probability': 6},
    {'id': 9, 'name': '外星人', 'icon': '👽', 'rarity': '史诗', 'probability': 4},
    {'id': 10, 'name': '法师', 'icon': '🧙', 'rarity': '史诗', 'probability': 3},
    {'id': 11, 'name': '金冠', 'icon': '👑', 'rarity': '传说', 'probability': 1.5},
    {'id': 12, 'name': '彩虹星', 'icon': '🌟', 'rarity': '传说', 'probability': 0.5}
]

# 刮刮乐符号
SCRATCH_SYMBOLS = ['💎', '⭐', '🍒', '🍋']
SCRATCH_PAYOUT = {
    ('💎', '💎', '💎'): 100,
    ('⭐', '⭐', '⭐'): 50,
    ('🍒', '🍒', '🍒'): 30,
    ('🍋', '🍋', '🍋'): 20
}


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html', games=GAMES_CONFIG)


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """重置游戏状态"""
    session['coins'] = 300
    session['gacha_collection'] = []
    session['updown_history'] = [random.randint(1, 100)]
    session['updown_current'] = session['updown_history'][-1]
    session.modified = True
    return jsonify({'success': True, 'coins': 300})


@app.route('/api/get_state', methods=['GET'])
def get_state():
    """获取当前游戏状态"""
    if 'coins' not in session:
        session['coins'] = 300
        session['gacha_collection'] = []
        session['updown_history'] = [random.randint(1, 100)]
        session['updown_current'] = session['updown_history'][-1]
    return jsonify({
        'coins': session['coins'],
        'gacha_collection': session.get('gacha_collection', [])
    })


@app.route('/api/slots', methods=['POST'])
def play_slots():
    """老虎机游戏"""
    data = request.json
    leverage = data.get('leverage', 1)

    cost = 5 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    # 生成随机结果
    result = []
    for _ in range(3):
        result.append(random.choice(SLOTS_SYMBOLS))

    # 计算奖励
    base_reward = calculate_slots_reward(result)
    actual_reward = base_reward * leverage

    if actual_reward > 0:
        session['coins'] += actual_reward

    session.modified = True

    return jsonify({
        'success': True,
        'result': result,
        'reward': actual_reward,
        'base_reward': base_reward,
        'leverage': leverage,
        'cost': cost,
        'coins': session['coins']
    })


def calculate_slots_reward(result):
    """计算老虎机奖励"""
    key = tuple(result)
    if key in SLOTS_PAYOUT:
        return SLOTS_PAYOUT[key]

    # 水果三连
    if all(s in FRUIT_SYMBOLS for s in result) and len(set(result)) == 1:
        return 40

    # 其他三连
    if len(set(result)) == 1:
        return 30

    # 特殊组合
    if result[0] == '🎰' and result[2] == '🎰':
        return 20
    if result[0] == '7️⃣' and result[1] == '7️⃣':
        return 15
    if result[0] == '💎' and result[1] == '💎':
        return 10

    # 任意两个高价值符号
    high_count = sum(1 for s in result if s in HIGH_VALUE_SYMBOLS)
    if high_count >= 2:
        return 5

    return 0


@app.route('/api/wheel', methods=['POST'])
def play_wheel():
    """幸运轮盘游戏"""
    data = request.json
    leverage = data.get('leverage', 1)

    cost = 3 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    # 随机选择扇形
    sector = random.choice(WHEEL_SECTORS)
    base_reward = sector['value']
    actual_reward = base_reward * leverage

    if actual_reward > 0:
        session['coins'] += actual_reward

    session.modified = True

    return jsonify({
        'success': True,
        'reward': actual_reward,
        'base_reward': base_reward,
        'leverage': leverage,
        'sector_value': base_reward,
        'sector_color': sector['color'],
        'coins': session['coins']
    })


@app.route('/api/chest', methods=['POST'])
def play_chest():
    """神秘宝箱游戏"""
    data = request.json
    leverage = data.get('leverage', 1)

    cost = 10 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    # 根据概率选择奖励
    rand = random.randint(1, 100)
    cumulative = 0
    base_reward = 0
    for reward, prob in CHEST_REWARDS:
        cumulative += prob
        if rand <= cumulative:
            base_reward = reward
            break

    actual_reward = base_reward * leverage

    if actual_reward > 0:
        session['coins'] += actual_reward

    session.modified = True

    return jsonify({
        'success': True,
        'reward': actual_reward,
        'base_reward': base_reward,
        'leverage': leverage,
        'coins': session['coins']
    })


@app.route('/api/updown', methods=['POST'])
def play_updown():
    """涨跌猜游戏"""
    data = request.json
    leverage = data.get('leverage', 1)
    guess = data.get('guess')  # 'up' or 'down'

    cost = 5 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    current = session.get('updown_current', random.randint(1, 100))

    # 生成新数字
    change = random.randint(1, 20)
    new_value = current + random.choice([-change, change])
    new_value = max(1, min(100, new_value))

    # 判断输赢
    won = False
    if guess == 'up' and new_value > current:
        won = True
    elif guess == 'down' and new_value < current:
        won = True

    if won:
        base_reward = 10
        actual_reward = base_reward * leverage
        session['coins'] -= cost
        session['coins'] += actual_reward
    else:
        actual_reward = 0
        session['coins'] -= cost

    # 更新历史
    history = session.get('updown_history', [])
    history.append(new_value)
    if len(history) > 10:
        history.pop(0)
    session['updown_history'] = history
    session['updown_current'] = new_value
    session.modified = True

    return jsonify({
        'success': True,
        'won': won,
        'current': current,
        'new_value': new_value,
        'reward': actual_reward,
        'leverage': leverage,
        'history': history,
        'coins': session['coins']
    })


@app.route('/api/gacha', methods=['POST'])
def play_gacha():
    """扭蛋机游戏"""
    data = request.json
    count = data.get('count', 1)  # 1 or 10

    if count == 1:
        cost = 15
    else:
        cost = 135

    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    results = []
    collection = session.get('gacha_collection', [])
    new_items = []

    # 十连抽保底机制
    guaranteed_rare = False
    if count == 10:
        guaranteed_rare = True

    for i in range(count):
        # 随机抽取
        if guaranteed_rare and i == 9:
            # 最后一次保证稀有以上
            rare_items = [item for item in GACHA_ITEMS if item['rarity'] in ['稀有', '史诗', '传说']]
            item = random.choice(rare_items)
        else:
            rand = random.random() * 100
            cumulative = 0
            item = GACHA_ITEMS[0]
            for gacha_item in GACHA_ITEMS:
                cumulative += gacha_item['probability']
                if rand <= cumulative:
                    item = gacha_item
                    break

        results.append(item)
        if item['id'] not in collection:
            collection.append(item['id'])
            new_items.append(item)

    # 额外奖励
    extra_reward = random.randint(50, 100) if count == 10 else random.randint(5, 15)
    session['coins'] += extra_reward

    session['gacha_collection'] = collection
    session.modified = True

    return jsonify({
        'success': True,
        'results': results,
        'new_items': new_items,
        'extra_reward': extra_reward,
        'collection': collection,
        'coins': session['coins']
    })


@app.route('/api/scratch/new', methods=['POST'])
def new_scratch_card():
    """生成新刮刮卡"""
    data = request.json
    leverage = data.get('leverage', 1)

    cost = 5 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    # 生成3x3网格
    grid = []
    for i in range(9):
        grid.append(random.choice(SCRATCH_SYMBOLS))

    session['scratch_grid'] = grid
    session['scratch_revealed'] = [False] * 9
    session['scratch_leverage'] = leverage
    session.modified = True

    return jsonify({
        'success': True,
        'grid': grid,
        'cost': cost,
        'leverage': leverage,
        'coins': session['coins']
    })


@app.route('/api/scratch/reveal', methods=['POST'])
def reveal_scratch_cell():
    """刮开单个格子"""
    data = request.json
    index = data.get('index')

    grid = session.get('scratch_grid', [])
    revealed = session.get('scratch_revealed', [])

    if index < len(revealed) and not revealed[index]:
        revealed[index] = True
        session['scratch_revealed'] = revealed
        session.modified = True

        # 检查是否中奖
        win_amount = check_scratch_win(grid, revealed)

        if win_amount > 0 and not session.get('scratch_paid', False):
            leverage = session.get('scratch_leverage', 1)
            actual_reward = win_amount * leverage
            session['coins'] += actual_reward
            session['scratch_paid'] = True
            session.modified = True
            return jsonify({
                'success': True,
                'symbol': grid[index],
                'win_amount': actual_reward,
                'all_revealed': all(revealed),
                'coins': session['coins']
            })

        return jsonify({
            'success': True,
            'symbol': grid[index],
            'win_amount': 0,
            'all_revealed': all(revealed),
            'coins': session['coins']
        })

    return jsonify({'success': False, 'message': '无效操作'})


def check_scratch_win(grid, revealed):
    """检查刮刮乐中奖"""
    # 检查行
    for row in range(3):
        start = row * 3
        if all(revealed[start:start + 3]):
            if len(set(grid[start:start + 3])) == 1:
                symbol = grid[start]
                for pattern, payout in SCRATCH_PAYOUT.items():
                    if symbol == pattern[0]:
                        return payout

    # 检查列
    for col in range(3):
        indices = [col, col + 3, col + 6]
        if all(revealed[i] for i in indices):
            if len(set(grid[i] for i in indices)) == 1:
                symbol = grid[indices[0]]
                for pattern, payout in SCRATCH_PAYOUT.items():
                    if symbol == pattern[0]:
                        return payout

    # 检查对角线
    if all(revealed[i] for i in [0, 4, 8]):
        if len(set(grid[i] for i in [0, 4, 8])) == 1:
            symbol = grid[4]
            for pattern, payout in SCRATCH_PAYOUT.items():
                if symbol == pattern[0]:
                    return payout

    if all(revealed[i] for i in [2, 4, 6]):
        if len(set(grid[i] for i in [2, 4, 6])) == 1:
            symbol = grid[4]
            for pattern, payout in SCRATCH_PAYOUT.items():
                if symbol == pattern[0]:
                    return payout

    return 0


@app.route('/api/lottery', methods=['POST'])
def play_lottery():
    """体育彩票游戏"""
    data = request.json
    leverage = data.get('leverage', 1)
    chosen_number = data.get('number')

    cost = 10 * leverage
    if session['coins'] < cost:
        return jsonify({'success': False, 'message': '游戏币不足'})

    session['coins'] -= cost

    # 摇出3个球
    balls = [random.randint(1, 20) for _ in range(3)]
    matches = sum(1 for ball in balls if ball == chosen_number)

    if matches == 3:
        base_reward = 200
    elif matches == 2:
        base_reward = 50
    elif matches == 1:
        base_reward = 10
    else:
        base_reward = 0

    actual_reward = base_reward * leverage

    if actual_reward > 0:
        session['coins'] += actual_reward

    session.modified = True

    return jsonify({
        'success': True,
        'balls': balls,
        'matches': matches,
        'reward': actual_reward,
        'base_reward': base_reward,
        'leverage': leverage,
        'coins': session['coins']
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)