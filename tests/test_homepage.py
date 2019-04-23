
from django.conf import settings
from tests.common_tools import template_used
from conference.tests.factories.fare import SponsorFactory


def test_get_homepage(db, client):
    url = '/'
    response = client.get(url)

    assert response.status_code == 200
    assert template_used(response, 'ep19/bs/homepage/home.html')
    assert template_used(response, 'ep19/bs/homepage/_venue.html')
    assert template_used(response, 'ep19/bs/homepage/_sponsors.html')
    assert template_used(response, 'ep19/bs/homepage/_schedule_overview.html')
    assert template_used(response, 'ep19/bs/header/_with_jumbotron.html')
    assert b'EuroPython 2019' in response.content


def test_homepage_doesnt_contain_sponsor_if_no_income(
    db, client
):
    sponsor = SponsorFactory(
        alt_text="Sponsor Alt Text", title_text="Sponsor Title Text"
    )

    url = "/"
    response = client.get(url)

    assert sponsor.alt_text not in response.content.decode()
    assert sponsor.title_text not in response.content.decode()


def test_homepage_doesnt_contain_sponsor_if_income_for_different_conference(
    db, client
):

    sponsor = SponsorFactory(
        alt_text="Sponsor Alt Text", title_text="Sponsor Title Text"
    )
    sponsor.sponsorincome_set.create(income=123, conference="whatever2020")

    url = "/"
    response = client.get(url)

    assert sponsor.alt_text not in response.content.decode()
    assert sponsor.title_text not in response.content.decode()


def test_homepage_contains_sponsors_if_income_for_current_conference(
    db, client
):
    sponsor = SponsorFactory(
        alt_text="Sponsor Alt Text", title_text="Sponsor Title Text"
    )
    sponsor.sponsorincome_set.create(
        income=123,
        conference=settings.CONFERENCE_CONFERENCE
    )
    url = "/"
    response = client.get(url)

    assert sponsor.alt_text in response.content.decode()
    assert sponsor.title_text in response.content.decode()


def test_homepage_contains_googleanalytics(db, client):
    url = '/'
    response = client.get(url)
    assert response.status_code == 200

    EPCON_2019_GA_ID = 'UA-60323107-5'
    # NOTE(artcz) this should probably go into a variable, but good enough for
    assert EPCON_2019_GA_ID in response.content.decode()