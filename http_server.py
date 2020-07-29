import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from game import Game
from deck import AllCards

all = AllCards()
game = Game()


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _html(self, message):
        content = f"{message}"
        return content.encode('utf8')

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html('Hello'))

    def do_POST(self):
        if 'Content-Length' not in self.headers.keys():
            response = json.dumps({'id': 'x', 'error': 'Empty request!'})
            self.wfile.write(self._html(response))
            return
        content_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_len)
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            response = json.dumps({'id': 'x', 'error': 'Wrong request!'})
            self.wfile.write(self._html(response))
            return

        player_id = data.get('id')
        if player_id not in [player.name for player in game.players]:
            response = json.dumps({'id': player_id, 'error': f'No player with name: {player_id}!'})
            self._set_headers()
            self.wfile.write(self._html(response))
            return

        player = game.get_player(player_id)
        response = handle_client_data(player, data)
        self._set_headers()
        self.wfile.write(self._html(response))


def run(server_class=HTTPServer, handler_class=S, addr='localhost', port=1643):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on {addr}:{port}...')
    httpd.serve_forever()


def handle_client_data(player, data):
    player_id = player.name

    message_type = data.get('type')
    if message_type == 'sync':
        response = {'id': player_id, 'type': 'sync',
                    'update': player.update_available,
                    'players_ready': game.get_ready_players(), 'move_ready': player.move_available,
                    'queue': 0,
                    'end_age': player.end_age,
                    'player_waiting': True if player.ready_to_built is not None else False,
                    'left_waiting': True if player.left_neighbor.ready_to_built is not None else False,
                    'right_waiting': True if player.right_neighbor.ready_to_built is not None else False}
    elif message_type == 'get_data':
        response = {'id': player_id, 'type': 'get_data',
                    'state': player.state,
                    'cards': [card.id for card in player.available_cards],
                    'wonder': player.wonder.id,
                    'left_neighbor': [player.left_neighbor.wonder.id, len(player.left_neighbor.available_cards),
                                      player.left_neighbor.state],
                    'right_neighbor': [player.right_neighbor.wonder.id, len(player.right_neighbor.available_cards),
                                       player.right_neighbor.state],
                    'vp': player.total_vp,
                    'money': game.get_player_neighbor_money(player),
                    'military': game.get_player_neighbor_military(player),
                    'wins': game.get_player_neighbor_wins(player), 'loses': game.get_player_neighbor_loses(player),
                    'age': game.age, 'round': game.round}
        player.update_available = False
    elif message_type == 'first_get_data':
        response = {'id': player_id, 'type': 'first_get_data',
                    'state': player.state,
                    'cards': [card.id for card in player.available_cards],
                    'built_cards': [card.id for card in player.built_cards],
                    'left_built_cards': [card.id for card in player.left_neighbor.built_cards],
                    'right_built_cards': [card.id for card in player.right_neighbor.built_cards],
                    'wonder': player.wonder.id,
                    'left_neighbor': [player.left_neighbor.wonder.id, len(player.left_neighbor.available_cards),
                                      player.left_neighbor.state],
                    'right_neighbor': [player.right_neighbor.wonder.id, len(player.right_neighbor.available_cards),
                                       player.right_neighbor.state],
                    'vp': player.total_vp,
                    'money': game.get_player_neighbor_money(player),
                    'military': game.get_player_neighbor_military(player),
                    'wins': game.get_player_neighbor_wins(player), 'loses': game.get_player_neighbor_loses(player),
                    'age': game.age, 'round': game.round}
        player.update_available = False
    elif message_type == 'get_move':
        if player.build_discarded is True:
            player.move_available = False
            response = {'id': player_id, 'type': 'get_move',
                        'player_built': player.last_built,
                        'left_neighbor_built': player.left_neighbor.last_built,
                        'right_neighbor_built': player.right_neighbor.last_built,
                        'money': [player.left_neighbor.money, player.money, player.right_neighbor.money],
                        'military': [player.left_neighbor.calulate_military(), player.calulate_military(), player.right_neighbor.calulate_military()],
                        'wins': [player.left_neighbor.military_wins, player.military_wins, player.right_neighbor.military_wins],
                        'loses': [player.left_neighbor.military_loses, player.military_loses, player.right_neighbor.military_loses],
                        'discarded': True}
        else:
            response = {'id': player_id, 'type': 'get_move',
                        'player_built': player.last_built,
                        'left_neighbor_built': player.left_neighbor.last_built,
                        'right_neighbor_built': player.right_neighbor.last_built,
                        'money': [player.left_neighbor.money, player.money, player.right_neighbor.money],
                        'military': [player.left_neighbor.calulate_military(), player.calulate_military(), player.right_neighbor.calulate_military()],
                        'wins': [player.left_neighbor.military_wins, player.military_wins, player.right_neighbor.military_wins],
                        'loses': [player.left_neighbor.military_loses, player.military_loses, player.right_neighbor.military_loses],
                        'discarded': False}
            player.move_available = False
            game.update_emitted_move(player)
    elif message_type == 'build':
        if player.state != 1:
            building = data.get('building')
            chosen = data.get('chosen')
            discard = data.get('discard')
            wonder = data.get('wonder')

            if wonder is True:
                if player.can_build_wonder(chosen):
                    success = True
                    player.state = 1
                    game.prepare_for_build(player, building, chosen, discard, wonder)
                else:
                    success = False
            elif discard is True:
                success = True
                player.state = 1
                game.prepare_for_build(player, building, chosen, discard, wonder)
            elif player.can_build_with_promotion(all.get_card_by_id(building)):
                success = True
                player.state = 1
                game.prepare_for_build(player, building, chosen, discard)
            elif player.can_build(all.get_card_by_id(building), chosen):
                success = True
                player.state = 1
                game.prepare_for_build(player, building, chosen, discard)
            else:
                success = False
        else:
            success = True

        response = {'id': player_id, 'type': 'build', 'status': success}
        if game.get_ready_players() == 3:
            game.build()
            game.move_ready()
    elif message_type == 'card_details':
        if 'card_id' not in data.keys():
            response = {'id': player_id, 'error': 'Invalid message'}
        else:
            card_id = data.get('card_id')

            response = {'id': player_id, 'type': 'card_details',
                        'resources_needed': all.get_card_cost(card_id),
                        'resources_available': game.check_player_resources(player, card_id),
                        'upgrade': game.check_upgrade(player, card_id),
                        'status': game.get_card_status(card_id)}
    elif message_type == 'get_discarded':
        response = {'id': player_id, 'type': 'get_discarded',
                    'discarded': [card.id for card in game.discarded]}
    elif message_type == 'build_discarded':
        card_id = data.get('card_id')

        response = {'id': player_id, 'type': 'build_discarded',
                    'status': True}
        player.build_discarded = False
        player.build(all.get_card_by_id(card_id))
        game.move_ready()
    elif message_type == 'wonder_details':
        wonder_id = data.get('wonder_id')

        response = {'id': player_id, 'type': 'wonder_details',
                    'stage': player.built_wonders,
                    'resources_needed': player.get_next_wonder_cost(),
                    'resources_available': game.check_player_resources(player, 0, wonder=True)}
    elif message_type == 'end_age':
        player.end_age = False
        response = {'id': player_id, 'type': 'end_age',
                    'player_battle': player.last_battle,
                    'left_battle': player.left_neighbor.last_battle,
                    'right_battle': player.right_neighbor.last_battle}
    elif message_type == 'end_game':
        # player.end_game = False
        response = {'id': player_id, 'type': 'end_game',
                    'players': [player.name, player.left_neighbor.name, player.right_neighbor.name],
                    'battles': player.military_wins - player.military_loses,
                    'money': player.money // 3,
                    'blue': player.calculate_blue_vp(),
                    'wonder': player.calculate_wonder_vp(),
                    'yellow': player.calculate_yellow_vp(),
                    'green': player.calculate_green_vp(),
                    'purple': player.calculate_purple_vp()}
    else:
        response = {'id': player_id, 'error': 'Invalid message'}
    return json.dumps(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify IP address"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=1643,
        help="Specify port"
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
