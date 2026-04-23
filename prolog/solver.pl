:- dynamic suspect/1.
:- dynamic room/1.
:- dynamic weapon/1.
:- dynamic clue_person_in_room/2.
:- dynamic clue_person_not_in_room/2.
:- dynamic clue_person_has_weapon/2.
:- dynamic clue_person_not_has_weapon/2.
:- dynamic clue_room_has_weapon/2.
:- dynamic clue_crime_not_in_room/1.
:- dynamic clue_crime_not_with_weapon/1.

:- consult('facts.pl').
:- use_module(library(lists)).

solve :-
    solve(Criminal, CrimeRoom, CrimeWeapon),
    format('Criminal: ~w~n', [Criminal]),
    format('Camera: ~w~n', [CrimeRoom]),
    format('Arma: ~w~n', [CrimeWeapon]).

solve(Criminal, CrimeRoom, CrimeWeapon) :-
    findall(S, suspect(S), Suspects),
    findall(R, room(R), Rooms),
    findall(W, weapon(W), Weapons),
    permutation(Rooms, AssignedRooms),
    permutation(Weapons, AssignedWeapons),
    assign_pairs(Suspects, AssignedRooms, AssignedWeapons, Assignments),
    valid_assignments(Assignments),
    member(assign(Criminal, CrimeRoom, CrimeWeapon), Assignments),
    \+ clue_crime_not_in_room(CrimeRoom),
    \+ clue_crime_not_with_weapon(CrimeWeapon).

assign_pairs([], [], [], []).
assign_pairs([S|ST], [R|RT], [W|WT], [assign(S, R, W)|Rest]) :-
    assign_pairs(ST, RT, WT, Rest).

valid_assignments([]).
valid_assignments([assign(Person, Room, Weapon)|Rest]) :-
    respects_person_room_clues(Person, Room),
    respects_person_weapon_clues(Person, Weapon),
    respects_room_weapon_clues(Room, Weapon),
    valid_assignments(Rest).

respects_person_room_clues(Person, Room) :-
    (clue_person_in_room(Person, ExpectedRoom) -> Room = ExpectedRoom ; true),
    \+ clue_person_not_in_room(Person, Room).

respects_person_weapon_clues(Person, Weapon) :-
    (clue_person_has_weapon(Person, ExpectedWeapon) -> Weapon = ExpectedWeapon ; true),
    \+ clue_person_not_has_weapon(Person, Weapon).

respects_room_weapon_clues(Room, Weapon) :-
    (clue_room_has_weapon(Room, ExpectedWeapon) -> Weapon = ExpectedWeapon ; true).