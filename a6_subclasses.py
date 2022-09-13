# a6_subclasses.py
# ssd74, jv442
# Sources/people consulted: NONE
# May 8th, 2022
# Skeleton by Prof. Lee, Apr 2022; typo in Ad Loop docstring fixed Apr 30 6pm.

from a6_classes import Song, Mix, Loop


class Ad(Song):
    """An Ad should NOT be added to the Song class's all_of_em variable,
    because they aren't legitimate Songs. For instance, we wouldn't want them
    displayed in a catalog of Songs.

    Every Ad has artist "[Advertiser]" (literally, with the square brackets.)

    Class attribute:
        all_of_em: list of all Ads that are created.

    Instance attributes:
        includes those for Songs.

    """
    all_of_em = []

    #JUSTIFICATION: BECAUSE THE ADS SHOULDNT BE DISPLAYED WITH THE SONG LIST,
    #THE SUBCLASS NEEDS TO HAVE ITS OWN CLASS VARIABLE DECLARED, ALSO NAMED all_of_em AS
    #SPECIFIED BY THE DOCSTRING.

    def __init__(self, t, yt=None):
        """A new Ad with title `t`, artist `[Advertiser]`, and url `yt`.

        Preconditions:
            t: non-empty string
            yt: URL string or None
        """
        self.title = t
        self.artist = "[Advertiser]"
        self.url = yt
        Ad.all_of_em.append(self)

    #JUSTIFICATION: TITLE AND URL ARE CREATED SIMILARLY TO SONG, BUT BECAUSE
    #ARTIST IS A GIVEN VALUE, THE PARAMETER IS CHANGED FROM THE PARENT CLASS, SO __INIT__
    #IS OVERRIDDEN FROM THE PARENT CLASS FOR THIS METHOD. ALL OTHER METHODS ARE
    #EQUIVALENT TO THOSE IN THE PARENT CLASS SONG, SO THEY ARE NOT OVERRIDDEN.


class AdLoop(Loop):
    """
    Like a Loop, except that it plays an Ad after every Song.  The Ads should
    appear in the order they occur in Ad.all_of_em.

    Example: suppose the source Mix has only two Songs, s1 and s2, and
    Ad.all_of_em has Ads a1, a2, a3, a4, a5.
    Then, the sequence of Songs occurring if one ran the play() method multiple
    times is:
       s1 a1 s2 a2 s1 a3 s2 a4 s1 a5 s2 a1 s1 a2 ... # typo fixed 4/30 (s2->s1)

    Instance attributes:
        Includes those of Loops.

    """
    def __init__(self, m, shuffle = False):
        """
        A new AdLoop with its `title` set to the title of `m`, `slist` set to
        a list that alternates between m.songs() and Ad.all_of_em, its
        `next_pos` set to 0.

        EXCEPTION: If `shuffle` is True, then random.shuffle() should be applied
        to the contents of `temp_slist` to put the contents of `s_list` in
        random order but maintain the alternating.

        Preconditions:
        `m` is a Mix (not None).
        `shuffle` is a boolean.
        """

        self.title = m.title
        self.slist = []

        self.next_pos = 0

        #JUSTIFICATION: SIMILAR TO THE PARENT CLASS, WE USE AN INIT METHOD TO
        #UPDATE THE TITLE IN MIX "m" TO HAVE THE AD TITLES. SLIST BECOMES AN
        #EMPTY LIST THAT WILL BE APPENDED.

        temp_slist = m.songs()
        if shuffle:
            random.shuffle(temp_slist)

        #JUSTIFICATION: IF THE LIST IS BEING SHUFFLED, temp_slist WILL USE THE
        #FUNCTON songs FROM THE PARENT CLASS, WHICH PUTS THE ITEMS OF THE LIST
        #IN A SPECIFIC ORDER AND SHUFFLE THE LIST.

        song_ind = 0
        ad_ind = 0
        if shuffle:
            random.shuffle(temp_slist)

        for ad in Ad.all_of_em:
            self.slist.append(temp_slist[song_ind])
            song_ind += 1
            if song_ind > len(temp_slist)-1:
                song_ind = 0
            self.slist.append(ad)
            ad_ind += 1
            if ad_ind > len(Ad.all_of_em)-1:
                ad_ind = 0

        #JUSTIFICATION: THIS FOR LOOP LOOPS THROUGH THE FIRST CYCLE OF AD
        #LOOP, ADDING ONE SONG AND AD EACH ITERATION SO THAT THE WHILE LOOPS
        #CONDITIONS WILL NOT IMMEDIATELY TEST TRUE.

        while song_ind != ad_ind:
            self.slist.append(temp_slist[song_ind])
            song_ind += 1
            if song_ind > len(temp_slist)-1:
                song_ind = 0
            self.slist.append(Ad.all_of_em[ad_ind])
            ad_ind += 1
            if ad_ind > len(Ad.all_of_em)-1:
                ad_ind = 0

        #JUSTIFICATION: THE WHILE LOOP WHILE LOOP FOR THE REMAINING CYCLES IT
        #WOULD TAKE FOR THE SONG AND AD LISTS TO RETURN TO INDEX 0 AT THE
        #SAME TIME.

    #JUSTIFICATION: THE ORDER OF THE ADS DOESN'T CHANGE IF THE USER DECIDES TO
    #SHUFFLE.

    #JUSTIFICATION: __init__ HAS BEEN OVERRIDDEN TO ACCOUNT FOR THE ADS BEING
    #INSERTED. SLIST IS INITIALLY DECLARED AS AN EMPTY LIST AND THE METHOD
    #APPENDS THE NEXT SONG AND AD IN EACH LIST RESPECTIVELY, REPEATED UNTIL
    #BOTH LISTS REACH THE SAME INDEX AT THE SAME ITERATION, TO ACCOUNT FOR
    #THE LISTS BEING DIFFERENT LENGTHS. ALL OTHER VARIABLES ARE INSTANTIATED
    #THE SAME AS THE PARENT CLASS LOOP. BECAUSE SLIST IS CHANGED, WE DIDN'T
    #CHANGE ANY OTHER METHOD BECAUSE THE DISPLAYING AND PROMPTING FUNCTIONS
    #SHOULD REMAIN THE SAME.
