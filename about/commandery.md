---
# Knights Templar Commandery page
layout: body
body_key: commandery
title: "Commandery of Knights Templar"
seo_title: "Knights Templar Commandery"
description: "The Commandery of Knights Templar of Montgomery County, Maryland, the final order joined in the York Rite, conferring three orders and one passing order."
breadcrumbs:
  - label: "About"
    href: "/about/"
  - label: "Commandery of Knights Templar"
cta:
  title: "Interested in the Knights Templar?"
  text: "If you are a Mason who has completed the Royal Arch degrees and would like to find out more about the Commandery, please get in touch."
---

The Knights Templar is the final order joined in the York Rite.

## Membership

Unlike the initial degrees conferred in a regular Masonic Lodge, which (in
most Regular Masonic jurisdictions) only require a belief in a Supreme Being
regardless of religious affiliation, the Knights Templar is one of several
additional Masonic Orders in which membership is open only to Freemasons who
declare they will protect and defend the Christian faith.

Membership in the Knights Templar is open to Masons who have completed their
Royal Arch and in some jurisdictions their Cryptic Degrees.

## A living memorial

This body is modeled on the historical Knights Templar to carry on the spirit
of their organization. Throughout history it has been claimed that Freemasonry
itself was founded by the Knights Templar or that the Knights Templar took
refuge in Freemasonry after their persecution. The Grand Encampment of the
United States acknowledges the existence of these theories but states that
there is no proof to justify such claims.

## Organization and orders

A local Knights Templar division is called a Commandery and operates under a
state level Grand Commandery as well as The Grand Encampment of the United
States. This is unique among Masonic bodies as most report to the state level
alone.

The Knights Templar confer three orders, and one passing order as opposed to
the standard degree system found elsewhere in Freemasonry, each with its own
history:

{% assign body_data = site.data.bodies.bodies | where: "key", page.body_key | first %}
{% assign body_degrees = body_data.degrees %}

<ol class="degree-list">
  {% for degree in body_degrees %}
  <li class="degree-list__item">
    <a class="degree-list__link" href="{{ degree.url }}">{{ degree.name }}</a>
    {% if degree.note %}
      <span class="degree-list__note">{{ degree.note }}</span>
    {% endif %}
  </li>
  {% endfor %}
</ol>

Their histories are indexed together on the
[degree histories](/about/degrees/) page.

The Commandery completes the York Rite, following the
[Chapter of Royal Arch Masons](/about/chapter/) and the
[Council of Cryptic Masons](/about/council/).
