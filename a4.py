# a4.py
# jv442, ssd74
# Sources/people consulted: NONE
# March 30th, 2022
# Skeleton by Prof. Lee, LJL2, Mar 2022

""" See CS1110 Spring '22 A4 writeup. """

from a4_classes import Song, Mix

def songs_in(m):
    """Returns: sorted list of all *distinct* Songs that can be reached by
    tracing through the contents of `m`.

    Two Songs count as non-distinct if they have the same title and artist.

    `m` itself should remain unchanged.

    Examples:
        Suppose we had a Mix whose contents was [a4_test.llee, a4_test.weird].

        The `llee` Mix contains, using the variable names from a4_test.py,
           s_ba, s_ds, s_np, s_dyc, s_lme .
        The `weird` Mix can be worked out to contain
            s_ttabeftbou, s_r, s_batj, s_br, s_tmbtp, s_pk, s_gib, s_oial,
            s_bdth, s_tmbtp2, s_bdth2, s_dyc, s_lme
        There are two Songs in common: s_dyc and s_lme.

        The result should be (since the default sort order for Songs is by
        artist, then title) the list of the following Songs, in this order:

            s_r:    Song 'Redbone' by Childish Gambino
            s_batj: Song 'Bennie and the Jets' by Elton John
            s_dyc:  Song 'Dance Yrself Clean' by LCD Soundsystem
            s_lme:  'Losing My Edge' by LCD Soundsystem
            s_ds:   'Divorce Song' by Liz Phair
            s_np    'Nana Party (Chuang 2021 live version)' by OJM [et al.]
            s_br:   'Bohemian Rhapsody' by Queen
            s_ba:   'Broken Arrow' by Robbie Robertson
            s_ttabeftbou: 'This Town Ain’t Big Enough for the Both of Us' by Sparks
            s_bdth: 'Burning Down the House' by Talking Heads
            s_gib   'Girlfriend is better' by Talking Heads
            s_oial: 'Once in a lifetime' by Talking Heads
            s_pk:   'Psycho Killer' by Talking Heads
            s_tmbtp:'This must be the place' by Talking Heads
            s_tmbtp2:'This Must be the Place' by The Lumineers
            s_bdth2 :'Burning Down the House' by Tom Jones and the Cardigans

    Precondition: m is a Mix (not None).
    """
    assert isinstance(m, Mix), "songs_in: input not a Mix. It is: "+repr(m)

    result_no_dups = []
    for r in m.contents:
        if isinstance(r, Song):
            if r not in result_no_dups:
                result_no_dups.append(r)
        else:
            x = songs_in(r)
            for i in x:
                if i not in result_no_dups:
                    result_no_dups.append(i)
    return sorted(result_no_dups)



def basic_mixes(m):
    """Returns: a sorted list of the Mixes that are "reachable" from `m`
    and whose `contents` list consists entirely of Songs.

    In other words, in the list it returns are the reachable sub-Mixes
    (or sub-sub-, or sub-sub-sub-...Mixes) that are not themselves recursive
    in structure.

    `m` itself can be in the returned list.

    Duplicates in the returned list are OK.

    Example: for the `weird` Mix in a4_test,
     * the "reachable" Mixes are:
       `weird` itself, `high`, `m_recs`, `th2`, `lcd`, `th`.
     * The Mixes that should be in the returned list are:
      `th`, `lcd`, and `high` (sorted by title).

    Precondition:
        m: a Mix (not None)
    """
    assert isinstance(m, Mix), "basic_mixes: input not a Mix. It is "+repr(m)

    count = 0
    for x in m.contents:
        if isinstance(x, Song):
            count+= 1
    if count == len(m.contents):
        return [m]
    else:
        mix_list = []
        for y in m.contents:
            if isinstance(y, Mix):
                mix_list += basic_mixes(y)
    return sorted(mix_list)




def mixes_with(s, mlist):
    """Returns: sorted list of *titles* of Mixes in `mlist` that Song `s` is in
        (either directly or through indirect chain of containment).

    Preconditions:
        s: a Song (not None)
        mlist: a non-empty list of Mixes

    Example:
     if `s` were a4_test.s_m (that is, the Song with title 'Mercy'),
     and `mlist` were [a4_test.cs1110picks, a4_test.sad, a4_test.th],
     then the output would be:
       ['CS1110 picks', "Gary's list", 'Sad songs']

     * The first two are a result of the Song titled 'Mercy' being in the Mix
      titled "Gary's list", which is in the Mix titled 'cs1110 picks'.

     * The third comes from the Song being in the Mix titled 'Sad songs'.

     * The Song 'Mercy' isn't in the Mix titled 'why the big suit', so no
     more entries are in the output.
    """
    assert isinstance(s, Song) and isinstance(mlist, list)
    for item in mlist:
        assert isinstance(item, Mix)


    output = []
    for mix in mlist:
        for item in mix.contents:
            mix_only_list = []
            if isinstance(item, Song):
                if item == s:
                    output+=[mix.title]
            else:
                curr_len = len(output)
                mix_only_list.append(item)
                output += mixes_with(s, mix_only_list)
                if len(output) > curr_len:
                    output += [mix.title]

    return sorted(set(output))
