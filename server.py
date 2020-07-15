import asyncio
import json
from random import randint
from game import Game
from deck import AllCards

all = AllCards()


async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        # try:
            print('REQ', request)
            request = (await reader.read(255)).decode('utf8')
            if request is None:
                writer.write(json.dumps({'id': 'x', 'error': 'No data!'}).encode('utf8'))
                await writer.drain()
                continue
            try:
                data = json.loads(request)
            except json.JSONDecodeError:
                writer.write(json.dumps({'id': 'x', 'error': 'Bad data!'}).encode('utf8'))
                await writer.drain()
                continue
            player_id = data.get('id')
            print(player_id)
            if player_id not in [player.name for player in game.players]:
                writer.write(json.dumps({'id': player_id, 'error': 'No player with with name!'}))
                await writer.drain()
                continue

            player = game.get_player(player_id)
            message_type = data.get('type')
            if message_type == 'sync':
                response = {'id': player_id, 'type': 'sync',
                            'update': player.update_available,
                            'players_ready': game.get_ready_players(), 'move_ready': player.move_available,
                            'queue': 0}
            elif message_type == 'get_data':
                response = {'id': player_id, 'type': 'get_data',
                            'state': player.state,
                            'cards': [card.id for card in player.available_cards],
                            'wonder': player.wonder.id,
                            'left_neighbor': [player.left_neighbor.wonder.id, len(player.left_neighbor.available_cards), player.left_neighbor.state],
                            'right_neighbor': [player.right_neighbor.wonder.id, len(player.right_neighbor.available_cards), player.right_neighbor.state],
                            'vp': player.total_vp, 'money': player.money, 'military': player.military_points,
                            'age': game.age, 'round': game.round}
                player.update_available = False
            elif message_type == 'get_move':
                response = {'id': player_id, 'type': 'get_move',
                            'player_built': 111,
                            'left_neighbor_built': 112,
                            'right_neighbor_built': 113,
                            'player_money_delta': 0}
                player.move_available = False
                game.update_emitted_move(player)
            elif message_type == 'build':
                success = True
                player.state = 1
                building = data.get('building')
                game.build(player, building)

                response = {'id': player_id, 'type': 'build', 'status': success}
                if game.get_ready_players() == 3:
                    game.move_ready()
            elif message_type == 'card_details':
                if 'card_id' not in data.keys():
                    response = {'id': player_id, 'error': 'Invalid message'}
                else:
                    card_id = data.get('card_id')

                    response = {'id': player_id, 'type': 'card_details',
                                'resources_needed': all.get_card_cost(card_id),
                                'resources': [],
                                'status': game.get_card_status(card_id)}
            else:
                response = {'id': player_id, 'error': 'Invalid message'}

            writer.write(json.dumps(response).encode('utf8'))
            await writer.drain()
        # except:
        #     print("Error")
    writer.close()

loop = asyncio.get_event_loop()
game = Game()

loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
loop.run_forever()
