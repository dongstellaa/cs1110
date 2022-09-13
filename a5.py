# a5_classes.py
# SSD74, JV442
# Sources/people consulted: NONE
# 04/12/2022
# Skeleton by Prof. Lee, LJL2, Mar 2022

"""(Re-)defines classes Song, Mix, and Loop, plus pretty-print function
pprint_mix() to aid in debugging.
"""

import webbrowser
import random

class Song:
    """Instance attributes:
        * title [non-empty string]: title of this Song.
        * artist [non-empty string]: name of artist(s) or group.
        * video [non-empty string or None]: if not None, is a
          link to YouTube video for the song

       Class variable:
        * all_of_em: list of all Songs that have been created.
    """
    all_of_em = [] 

    def __init__(self, t, a, yt=None):
        """A new Song with title `t`, artist `a`, youtube link 'yt'.

        Preconditions:
            t: non-empty string
            a: non-empty string
            yt: URL string for a YouTube video or None

        """
        self.title = t
        self.artist = a
        self.video = yt
        Song.all_of_em.append(self)

    def __eq__(self, other):
        return (isinstance(other, Song) and
                self.title == other.title and
                self.artist == other.artist and
                self.video == other.video)

    def __lt__(self, other):
        """Sort by artist, then by title. """
        assert isinstance(other, Song)
        return self.artist < other.artist or \
            (self.artist == other.artist and self.title < other.title)

    def __repr__(self):
        outstr = "Song '"+self.title+"' by "+self.artist
        if self.video is not None:
            outstr += ". Has a video"
        else:
            outstr += ". No video"
        return outstr

    def play(self):
        """
        If this Song has a video, launch it in a browser tab/window;
        otherwise, print "(No video available)"
        """
        if self.video is not None:
            webbrowser.open(self.video, new=0)
        else:
            print("(No video available)")


class Mix:
    """Instance Attributes:
        * title [non-empty string]: title of this Mix.
        * contents [non-empty list]: each element is either a Song (not None)
            or a Mix.  No cycles/loops in the containment relationships of
            any of the contents of the Mixes reachable from a given Mix's
            contents, including the Mix itself.

       Class variable:
        * all_of_em: list of all Mixes that have been created
    """

    all_of_em = []

    def __init__(self, t, c):
        """A new Mix with title `t` and contents `c`.

        Preconditions:
            t: non-empty string
            c: non-empty list.  Each element is either a Song (not None) a
              or a Mix.
        """
        self.title = t
        self.contents = c
        Mix.all_of_em.append(self)

    def __add__(self, other):
        assert isinstance(other, Mix)
        new_title = self.title + ' + ' + other.title
        new_contents = [self, other]
        return Mix(new_title, new_contents)


    def __eq__(self, other):
        return (isinstance(other, Mix) and
                self.title == other.title and
                self.contents == other.contents)

    def __lt__(self, other):
        """Sort by title."""
        assert isinstance(other, Mix)
        return self.title < other.title

    def __repr__(self):
        """Printout uses indents to indicate sub-items."""
        return pprint_mix_helper(self, '  ')

    def songs(self, keep_dups=False):
        """Returns a list of Songs in this Mix.

        The list should be ordered thusly:
           * the first set of elements is all the Songs represented by the
             first item (a Song or itself a Mix) in this Mix's contents,
           * the second set is all the Songs represented by the second item
             in this Mix's contents.
           * etc.

        If `keep_dups` is True, then repeated Songs are included in the returned
        list; otherwise, a repeated Song occurs only once, in its leftmost
        possible position.

        Example using the variables in file a5_music.py:
           if m is Mix('duplicates2', [llee, weird]), then

           m.songs() ->
           [s_ba, s_ds, s_np, s_dyc, s_lme, s_ttabeftbou, s_r, s_batj, s_br,
            s_tmbtp, s_pk, s_gib, s_oial, s_bdth, s_tmbtp2, s_bdth2]
           m.songs(keep_dups=True) ->
           [s_ba, s_ds, s_np, s_dyc, s_lme, s_ttabeftbou, s_r, s_batj, s_br,
            s_tmbtp, s_pk, s_gib, s_oial, s_bdth, s_tmbtp2, s_bdth2, s_dyc, s_lme]
        Preconditions: keep_dups is a Boolean
        """

        result = []
        for r in self.contents:
            if isinstance(r, Song):
                if (keep_dups is True) or (r not in result):
                    result.append(r)
            else:
                y = Mix.songs(r)
                for i in y:
                    if (keep_dups is True) or (i not in result):
                        result.append(i)
        return result

class Loop:
    """
    A Loop is an individual's execution of a Mix, an infinite loop until the
    user requests the Loop to end.

    The idea is that two people A and B might have be simultaneously listening
    to Songs from the same Mix m; but A might be on the 5th Song, and B might
    be on the 17th. So, we have different Loop objects to represent these two
    different viewing states.

    Instance attributes:
        title [str]: title of the Mix this Loop was derived from.
        slist: a non-empty list of Songs.
        next_pos [int]: position/index in `slist` of the *next* Song to play.
           It is always a valid index for `slist`.

    """

    def __init__(self, m, shuffle = False):
        """
        A new Loop with its `slist` set to m.songs(), its `title` set to the
        title of `m`, and its `next_pos` set to 0.

        EXCEPTION: If `shuffle` is True, then random.shuffle() should be applied
        to the contents of `slist` to put it in random order.

        Preconditions:
        `m` is a Mix (not None).
        `shuffle` is a boolean.
        """

        self.mix = m
        self.title = m.title
        self.slist = m.songs()
        self.next_pos = 0
        if shuffle is True:
            random.shuffle(self.slist)

    def _prompt(self):
        """Returns string
            'Hit Enter/Return to start the next video, ' + \
            '<next song's title> by <next song's artist>, or "q" to quit: '
           where the stuff in angle brackets should be replaced by the reasonable
           thing.
        """
        next_song = self.slist[self.next_pos]
        return 'Hit Enter/Return to start the next video, ' + next_song.title + ' by ' + next_song.artist + ', or "q" to quit: '


    def play(self):
        """
        1. Print the title of this Loop.

        2. continuously query the user if they want to play the next Song.
        If the last Song has been reached, the next song is the *first* Song
        in this Loop's slist.

        Response of `q` means quit, any other response means play the next
        Song."""

        print('Starting Loop '+self.title)
        response=input(self._prompt())
        while 'q' not in response:
            play_song = self.slist[self.next_pos]
            play_song.play()
            if len(self.slist) == self.next_pos+1:
                self.next_pos = 0
            else:
                self.next_pos += 1
            response=input(self._prompt())
        print('Exiting this Loop')



def pprint_mix(m):
    """Pretty-print Mix `m`.  Returns None.

    Example: In a4_test, pretty-printing Mix `weird` would print the following:

    Mix 'Eccentrica' with contents:
      Mix 'Songs in the key of Falsetto' with contents:
        Song 'This Town Ain’t Big Enough for the Both of Us'
        Song 'Redbone'
        Song 'Bennie and the Jets'
        Song 'Bohemian Rhapsody'
      Mix 'Recs from M' with contents:
        Mix 'Talking Heads Songs and Covers' with contents:
          Mix 'why the big suit' with contents:
            Song 'This must be the place'
            Song 'Psycho Killer'
            Song 'Girlfriend is better'
            Song 'Once in a lifetime'
            Song 'Burning Down the House'
          Song 'This Must be the Place'
          Song 'Burning Down the House'
        Mix 'LCD Soundsystem' with contents:
          Song 'Dance Yrself Clean'
          Song 'Losing My Edge'

    which reflects that
    `weird` contains:
      Mix `high`
      and Mix `m_recs` which contains:
         Mix `th2` which contains
            Mix `th`
         and Mix `lcd`

    """
    print(pprint_mix_helper(m, '  '))



def pprint_mix_helper(m, prefix):
    """Returns a string representing Mix `m`, with each content item
        indented one `prefix` in for each level of nesting.

    Preconditions:
      m is a Mix (not None).
      `prefix` is a string. Expected to be something like a tab (\t) or spaces.
    """
    out = "Mix '"+m.title+"' with contents:\n"
    for item in m.contents:
        if isinstance(item, Song):
            out += prefix+"Song '"+item.title+ "'\n"
        else:
            assert isinstance(item, Mix), "Bad item in contents, namely, "+repr(item)


            itemlines = pprint_mix_helper(item, prefix).strip().split("\n")
            for line in itemlines:
                out += (prefix+line+"\n")
    return out
