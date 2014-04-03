def genres(genre, duration):

    from generators.slow import slow
    from generators.soft import soft
    from generators.fast import fast
    from generators.hardcore import hardcore
    from generators.extreme import extreme
    from generators.drop_bass import drop_bass

    types = {
        "slow" : slow,
        "soft" : soft,
        "fast" : fast,
        "hardcore" : hardcore,
        "extreme" : extreme,
        "drop bass" : drop_bass
    }

    return types[genre](duration)
