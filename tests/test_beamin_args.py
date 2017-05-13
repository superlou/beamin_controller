from beamin_controller.beamin import parse_args
import pytest


def test_basic_args():
    assert parse_args(['--start']).start == True
    assert parse_args(['-s']).start == True

    assert parse_args(['--stop']).stop == True
    assert parse_args(['-x']).stop == True

    assert parse_args(['--list']).list == True
    assert parse_args(['-l']).list == True


def test_stop_and_start_args_cannot_both_be_supplied():
    with pytest.raises(SystemExit):
        args = parse_args(['--start', '--stop'])

    with pytest.raises(SystemExit):
        args = parse_args(['--stop', '--start'])


def test_assert_push_args():
    args = parse_args([])
    assert args.push == None

    args = parse_args(['--push'])
    assert args.push == ['default']

    args = parse_args(['--push', 'group1'])
    assert args.push == ['group1']

    args = parse_args(['--push', 'group1', 'group2'])
    assert args.push == ['group1', 'group2']

    args = parse_args(['--push', 'group1', '--push', 'group2'])
    assert args.push == ['group1', 'group2']
