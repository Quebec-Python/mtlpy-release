#!/usr/bin/env python
# -*- coding: UTF8 -*-
import sys
import os
import re
import codecs
import json
from random import choice
from argparse import ArgumentParser

fichiers = [
    'fr.adj',
    'fr.nom',
]

def parse_args():
    """Parsing des arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("lettre",
                        help="Lettre initiale")
    parser.add_argument("-n", "--nombre", type=int, default=1,
                        help=u"Nombre de noms à générer")
    return parser.parse_args()


def telecharge_wolf():
    """
    Télécharge WOLF - wordnet français dans le répertoire courant.
    Nécessite wget.
    """
    os.system(
        'wget https://gforge.inria.fr/frs/download.php/27165/wolf-0.1.5.xml.gz '
        '&& gunzip wolf-0.1.5.xml.gz'
    )


def parse_wolf():
    """
    Parse le fichier WOLF en fr.adj et fr.nom
    """
    adjs, noms = [], []
    r = re.compile(r"<LITERAL>(.+?)<")
    with codecs.open('wolf-0.1.5.xml', 'r', 'utf-8') as f:
        for ligne in f:
            if '-a</ID>' in ligne:
                m = r.search(ligne)
                if m:
                    adjs.append(m.groups()[0].strip())
            if '-n</ID>' in ligne:
                m = r.search(ligne)
                if m:
                    noms.append(m.groups()[0].strip())

    adjs = sorted(set(adjs))
    noms = sorted(set(noms))

    with codecs.open('fr.adj', 'w', 'utf-8') as f:
        json.dump(adjs, f)
    with codecs.open('fr.nom', 'w', 'utf-8') as f:
        json.dump(noms, f)

    return adjs, noms


def parse_json():
    """Récupère les fichiers générés précédemment."""
    resultat = []
    for fichier in fichiers:
        with codecs.open(fichier, 'r', 'utf-8') as f:
            resultat.append(json.load(f))

    return resultat


def affiche_noms(adjs, noms, args):
    """Génère et affiche des noms"""
    adjs = [x for x in adjs if x.startswith(args.lettre)]
    noms = [x for x in noms if x.startswith(args.lettre)]
    for i in range(args.nombre):
        print("{} {}".format(
            choice(adjs),
            choice(noms),
        ))
    

def main():
    if not all(os.path.exists(fichier) for fichier in fichiers):
        telecharge_wolf()
        adjs, noms = parse_wolf()
    else:
        adjs, noms = parse_json()

    args = parse_args()
    affiche_noms(adjs, noms, args)


if __name__ == '__main__':
    main()

