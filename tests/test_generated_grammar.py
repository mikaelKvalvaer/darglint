r"""Tests for a grammar generated by bnf_to_cnf, using cyk.

Original grammar:

    <start> ::= <sentence>

    <sentence> ::=
          <trans_verb_phrase>
        | <noun_phrase> <trans_verb_phrase>
        | <intrans_verb_phrase>

    <intrans_verb_phrase> ::=
          <intransitive_verb> <noun_phrase>
        | <intransitive_verb>

    <trans_verb_phrase> ::=
          <transitive_verb> <noun_phrase>
        | <transitive_verb>

    <noun_phrase> ::=
          <noun>
        | <noun> <adjective>
        | <noun> <noun>
        | <noun> <adjective> <noun>
        | <noun> <noun> <adjective>

    <intransitive_verb> ::= "GTT\.intransitive_verb"
    <transitive_verb> ::= "GTT\.transitive_verb"
    <noun> ::= "GTT\.noun"
    <adjective> ::= "GTT\.adjective"


# Where the following tokens are lexed.

    <intransitive_verb> ::=
          "Hegh"
        | "quS"

    <transitive_verb> ::=
          "HoH"
        | "qIp"

    <noun> ::=
          "Duj"
        | "loD"
        | "puq"
        | "bIQ"

    <adjective> ::=
          "val"
        | "QIp"

"""

from unittest import TestCase

from darglint.parse.grammar import BaseGrammar
from darglint.parse.grammar import Production as P
from darglint.parse.cyk import parse
from darglint.token import (
    BaseTokenType,
    Token,
)


class GTT(BaseTokenType):

    intransitive_verb = 0
    transitive_verb = 1
    noun = 2
    adjective = 3

    unknown = 4


# Generated on 2019-04-14 12:25:50.959489
class Grammar(BaseGrammar):
    productions = [
        P("start", ("intransitive_verb", "noun_phrase"),
            GTT.intransitive_verb, ("noun_phrase", "trans_verb_phrase"),
            ("transitive_verb", "noun_phrase"), GTT.transitive_verb),
        P("trans_verb_phrase", ("transitive_verb", "noun_phrase"),
            GTT.transitive_verb),
        P("noun_phrase", ("noun", "adjective"), ("noun", "noun"),
            ("noun", "noun_phrase0"), ("noun", "noun_phrase1"), GTT.noun),
        P("intransitive_verb", GTT.intransitive_verb),
        P("transitive_verb", GTT.transitive_verb),
        P("noun", GTT.noun),
        P("adjective", GTT.adjective),
        P("noun_phrase0", ("adjective", "noun")),
        P("noun_phrase1", ("noun", "adjective")),
    ]

    start = "start"


def _lex(sentence):
    lookup = {
        "Hegh": GTT.intransitive_verb,
        "quS": GTT.intransitive_verb,
        "HoH": GTT.transitive_verb,
        "qIp": GTT.transitive_verb,
        "Duj": GTT.noun,
        "loD": GTT.noun,
        "puq": GTT.noun,
        "bIQ": GTT.noun,
        "val": GTT.adjective,
        "QIp": GTT.adjective,
    }
    for word in sentence.split():
        yield Token(
            value=word,
            token_type=lookup.get(word, GTT.unknown),
            line_number=0,
        )


def lex(sentence):
    return list(_lex(sentence))


class GeneratedGrammarTest(TestCase):

    def test_valid_sentences(self):
        sentences = [
            "Hegh puq",
            "loD HoH puq Duj",
            "qIp bIQ QIp",
            "puq val qIp loD",
        ]
        for sentence in sentences:
            self.assertTrue(
                parse(Grammar, lex(sentence)),
                'Expected to parse "{}", but failed.'.format(
                    sentence
                )
            )

    def test_invalid_sentences(self):
        bad_sentences = [
            # Unrecognized symbol
            "unrecognized puq"

            # Incorrect structure
            "qIp qIp"
        ]
        for sentence in bad_sentences:
            self.assertFalse(
                parse(Grammar, lex(sentence)),
                'Unexpectedly parsed "{}"'.format(
                    sentence,
                )
            )