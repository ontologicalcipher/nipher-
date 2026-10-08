def run(target):
    from nipher.modules.domain import run as domain
    from nipher.modules.web import run as web

    return {
        "module":"report",
        "target":target,
        "domain":domain(target),
        "web":web(target)
    }
