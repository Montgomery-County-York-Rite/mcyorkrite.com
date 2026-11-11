---
# About the York Rite — Montgomery County
layout: page
title: "About the York Rite"
lede: "The Montgomery County York Rite family — three appendant bodies, one continuing Masonic story."
description: "About the Montgomery County York Rite: the Chapter of Royal Arch Masons, the Council of Cryptic Masons, and the Commandery of Knights Templar, and how they fit together."
breadcrumbs:
  - label: "About"
seo_title: "About"
---

## What is the York Rite?

The Montgomery County York Rite is a collection of Appendant Bodies that
operate independently of each other. Each body continues the Masonic story
beyond the three degrees of the Symbolic Lodge, and each confers its own
degrees or orders.

If you are a Master Mason in good standing from a regular Jurisdiction, you
may be eligible to join.

## The three bodies

<div class="body-grid body-grid--compact">
  {%- for body in site.data.bodies.bodies -%}
    {% include body-card.html body = body %}
  {%- endfor -%}
</div>

## How the bodies relate

The three bodies form a recognized progression within the Rite:

<ol class="progression-steps">
  {%- for body in site.data.bodies.bodies -%}
  <li class="progression-step progression-step--{{ body.accent }}">
    <span class="progression-step__ordinal">{{ body.ordinal }}</span>
    <span class="progression-step__name">{{ body.order_name }}</span>
    <span class="progression-step__body">{{ body.short_name }}</span>
    <a class="progression-step__link arrow-link" href="{{ body.url }}">Learn more<span class="visually-hidden"> — about {{ body.name }}</span></a>
  </li>
  {%- endfor -%}
</ol>

- **The Chapter confers the Capitular degrees.** Royal Arch Masonry is the
  first part of the York Rite system of the Masonic degrees.
- **The Council confers the Cryptic degrees.** Cryptic Masonry is the second
  part of the York Rite system of Masonic degrees.
- **The Commandery confers the Templar orders.** The Knights Templar is the
  final order joined in the York Rite.

Each body is separately constituted and operates independently, while the
three together make up the York Rite family in Montgomery County.

{% include keystone-divider.html %}

## Visit us

The bodies meet at {{ site.data.organization.meeting_location.lodge }} in
{{ site.data.organization.meeting_location.city }}, Maryland. See the
[contact page](/contact/) for the address, directions, and meeting times, or
check the [events calendar](/events/) for upcoming activities.
