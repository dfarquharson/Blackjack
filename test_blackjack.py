import unittest

from blackjack import *


class MiscTest(unittest.TestCase):
    def test_constant_random_element(self):
        self.assertEquals(1, random_element([1]))

    def test_actual_random_element_small(self):
        self.assertTrue(random_element([1, 2, 3]) in [1, 2, 3])

    def test_actual_random_element_large(self):
        self.assertTrue(random_element(range(10000)) in range(10000))


class ValueTest(unittest.TestCase):
    def test_value(self):
        self.assertEquals(11, Value.ACE.value)
        self.assertEquals(10, Value.KING.value)
        self.assertEquals(10, Value.QUEEN.value)
        self.assertEquals(10, Value.JACK.value)
        self.assertEquals(9, Value.NINE.value)
        self.assertEquals(2, Value.TWO.value)

    def test_equality(self):
        self.assertEquals(Value.ACE, Value.ACE)
        # face cards all have the same value in blackjack
        self.assertEquals(Value.KING, Value.QUEEN)
        self.assertNotEquals(Value.TWO, Value.THREE)


class CardTest(unittest.TestCase):
    def test_equality(self):
        self.assertEquals(Card(Value.ACE, Suit.CLUBS),
                          Card(Value.ACE, Suit.CLUBS))
        self.assertEquals(Card(Value.TEN, Suit.CLUBS),
                          Card(Value.JACK, Suit.CLUBS))
        self.assertNotEquals(Card(Value.TWO, Suit.HEARTS),
                             Card(Value.TWO, Suit.SPADES))


class HandTest(unittest.TestCase):
    def test_strength(self):
        self.assertEquals(Strength.HARD, Hand(
            [Card(Value.TWO),
             Card(Value.NINE)]).get_strength())
        self.assertEquals(Strength.SOFT, Hand(
            [Card(Value.ACE),
             Card(Value.TEN)]).get_strength())

    def test_value(self):
        self.assertEquals(21, Hand(
            [Card(Value.ACE),
             Card(Value.TEN)]).get_value())
        val = Hand([Card(), Card()]).get_value()
        # TODO: handle case where hand is 2 aces
        # this generally requires smart handling of soft hands.
        self.assertTrue(val < 22)

    def test_soft_hand_value(self):
        self.assertEqual(17, Hand([Card(Value.ACE),
                                   Card(Value.SIX)]).get_value())
        # self.assertEqual(18, Hand([Card(Value.ACE),
        #                            Card(Value.SIX),
        #                            Card(Value.ACE)]).get_value())


class PlayerTest(unittest.TestCase):
    def test_place_bet(self):
        p1 = Player()
        self.assertEquals(0, p1.pending_bet)
        p1.place_bet(10)
        self.assertEquals(10, p1.pending_bet)

    def test_hit(self):
        p1 = Player()
        num_cards = len(p1.hand.cards)
        p1.hit()
        self.assertEquals(num_cards + 1, len(p1.hand.cards))

    def test_active(self):
        self.assertTrue(Player().is_active())
        self.assertFalse(Player(money=0).is_active())
        self.assertTrue(Player(money=100).is_active())
        self.assertFalse(Player(money=-100).is_active())

    def test_is_bust(self):
        self.assertTrue(Player(hand=Hand([Card(Value.TEN),
                                          Card(Value.TEN),
                                          Card(Value.TWO)])).is_bust())
        self.assertFalse(Player(hand=Hand([Card(Value.TEN),
                                           Card(Value.NINE),
                                           Card(Value.TWO)])).is_bust())
        self.assertFalse(Player(hand=Hand([Card(Value.ACE)])).is_bust())
        # TODO: add a case where a soft ACE prevents the bust
        self.assertFalse(Player().is_bust())

    def test_should_hit(self):
        self.assertTrue(Player().should_hit())
        self.assertFalse(Player(hand=Hand([Card(Value.TEN),
                                           Card(Value.TEN)])).should_hit())
        self.assertTrue(Player(hand=Hand([Card(Value.FIVE),
                                          Card(Value.FIVE)])).should_hit())

    def test_should_stay(self):
        self.assertFalse(Player().should_stay())
        self.assertTrue(Player(hand=Hand([Card(Value.TEN),
                                          Card(Value.TEN)])).should_stay())
        self.assertFalse(Player(hand=Hand([Card(Value.FIVE),
                                           Card(Value.FIVE)])).should_stay())

    def test_handle_result_win(self):
        p1 = Player(hand=Hand([Card(Value.TEN), Card(Value.ACE)]))
        starting_money = p1.money
        bet = 10
        p1.place_bet(bet)
        p1.handle_result(19)
        self.assertEqual(starting_money + bet, p1.money)
        self.assertEqual(Hand(), p1.hand)
        self.assertEqual(0, p1.pending_bet)

    def test_handle_result_lose(self):
        p1 = Player(hand=Hand([Card(Value.TWO), Card(Value.TWO)]))
        starting_money = p1.money
        bet = 10
        p1.place_bet(bet)
        p1.handle_result(19)
        self.assertEqual(starting_money - bet, p1.money)
        self.assertEqual(Hand(), p1.hand)
        self.assertEqual(0, p1.pending_bet)

    def test_handle_result_bust(self):
        p1 = Player(hand=Hand([Card(Value.TEN),
                               Card(Value.TWO),
                               Card(Value.KING)]))
        starting_money = p1.money
        bet = 10
        p1.place_bet(bet)
        p1.handle_result(22)
        self.assertEqual(starting_money - bet, p1.money)
        self.assertEqual(Hand(), p1.hand)
        self.assertEqual(0, p1.pending_bet)

    def test_increment_rounds_survived(self):
        p1 = Player(money=0)
        p1.__increment_rounds_survived__()
        self.assertEqual(0, p1.rounds_survived)

    def test_get_stats(self):
        p1 = Player()
        stats = p1.get_stats()
        self.assertEqual(15, stats['hit_threshold'])
        self.assertEqual(0, stats['rounds_survived'])


class DealerTest(unittest.TestCase):
    def test_deal(self):
        dealer = Dealer()
        p1 = Player()
        p2 = Player()
        dealer.deal([p1, p2])
        for p in [dealer, p1, p2]:
            self.assertEqual(2, len(p.hand.cards))

    def test_show_present(self):
        dealer = Dealer()
        dealer.deal([])
        self.assertTrue(isinstance(dealer.show(), Card))

    def test_show_nothing(self):
        self.assertEqual(None, Dealer().show())

    def test_should_hit(self):
        self.assertTrue(Dealer(hand=Hand([Card(Value.KING),
                                          Card(Value.SIX)])).should_hit())
        self.assertFalse(Dealer(hand=Hand([Card(Value.KING),
                                           Card(Value.SEVEN)])).should_hit())
        self.assertFalse(Dealer(hand=Hand([Card(Value.KING),
                                           Card(Value.KING),
                                           Card(Value.TWO)])).should_hit())


class GameTest(unittest.TestCase):
    def test_has_active_players_true(self):
        g = Game([Player(), Player()])
        self.assertTrue(g.has_active_players())

    def test_has_active_players_false(self):
        g = Game([Player(money=0)])
        self.assertFalse(g.has_active_players())

    def test_players_bet(self):
        p1 = Player()
        g = Game([p1], 20)
        self.assertEqual(0, p1.pending_bet)
        g.players_bet()
        self.assertEqual(20, p1.pending_bet)

    def test_setup_game(self):
        p1, p2 = Player(), Player()
        g = Game([p1, p2])
        self.assertEqual([0, 0], [len(x.hand.cards) for x in [p1, p2]])
        g.setup_game()
        self.assertEqual([2, 2], [len(x.hand.cards) for x in [p1, p2]])

    def test_player_play(self):
        Game.player_play(Player(money=0))
        Game.player_play(Player())

    def test_play(self):
        Game([Player(), Player()]).play()
