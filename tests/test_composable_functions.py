from composable.functions import I, _ComposableFunction, composable as c, compose, rcompose
from functools import partial, reduce

def add_one(x: int) -> int:
    return x + 1


def add_two(x: int) -> int:
    return x + 2


def times_two(x: int) -> int:
    return x * 2


class TestComposable:
    def test_wraps_correctly_single_function(self):
        fn = c(add_one)
        assert isinstance(fn, _ComposableFunction)
        assert fn(5) == add_one(5)

    def test_wraps_correctly_single_function(self):
        fn = c(add_one)
        assert isinstance(fn, _ComposableFunction)
        assert fn(5) == add_one(5)

    def test_can_forward_compose_two_functions(self):
        fn = c(add_one) >> times_two
        assert fn(5) == times_two(add_one(5))

    def test_can_forward_compose_multiple_functions(self):
        fn = c(add_one) >> times_two >> add_two
        assert fn(5) == add_two(times_two(add_one(5)))

    def test_forward_composing_with_identity_produces_the_same_function(self):
        assert (c(add_one) >> I)(5) == add_one(5)
        assert (I >> add_one)(5) == add_one(5)

    def test_can_backwards_compose_two_functions(self):
        fn = c(add_one) << times_two
        assert fn(5) == add_one(times_two(5))

    def test_can_backwards_compose_multiple_functions(self):
        fn = c(add_one) << times_two << add_two
        assert fn(5) == add_one(times_two(add_two(5)))

    def test_backwards_composing_with_identity_produces_the_same_function(self):
        assert (c(add_one) << I)(5) == add_one(5)
        assert (I << add_one)(5) == add_one(5)
    
    def test_more_interesting_pipelines_can_be_built(self):
        line = "Composition is very noice"
        word_counter = (
            I>> str.strip
            >> str.split
            >> len
        )
        assert word_counter(line) == 4
    
    def test_mapreduce_wordcount_with_composing(self):
        stream = (
            "lorem ipsum dolor",
            "sit amet, consectetur adipiscing elit",
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
        )
        count_words = (
            I>> partial(map, str.split)
            >> partial(map, len)
            >> sum
        )
        assert count_words(stream) == 19


class TestCompose:
    def test_no_args_returns_identity(self):
        assert compose() == I
        assert rcompose() == I

    def test_single_function_only_wraps_it(self):
        assert compose(add_one)(1) == add_one(1)
        assert rcompose(add_one)(1) == add_one(1)

    def test_forward_compose_composes_functions_in_right_order(self):
        fn = compose(add_one, add_two, times_two)
        assert fn(5) == (add_one(add_two(times_two(5))))

    def test_backward_compose_composes_functions_in_right_order(self):
        fn = rcompose(add_one, add_two, times_two)
        assert fn(5) == (times_two(add_two(add_one(5))))
    
    def test_pipe(self):
        
        val = [1,2,3,4] | (
            I>> partial(map, lambda x: x + 1)
            >> partial(map, lambda x: x + 1)
        )
        assert list(val) == [3,4,5,6]
