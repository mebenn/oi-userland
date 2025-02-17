#
# This file and its contents are supplied under the terms of the
# Common Development and Distribution License ("CDDL"), version 1.0.
# You may only use this file in accordance with the terms of version
# 1.0 of the CDDL.
#
# A full copy of the text of the CDDL should have accompanied this
# source.  A copy of the CDDL is also available via the Internet at
# http://www.illumos.org/license/CDDL.
#

#
# Copyright 2015 Alexander Pyhalov
#

BUILD_STYLE=configure
BUILD_BITS=32_and_64
include ../../../../make-rules/shared-macros.mk

COMPONENT_NAME=         at-spi2-core
COMPONENT_VERSION=      2.24.1
COMPONENT_REVISION=     2
COMPONENT_SUMMARY=      Assistive Technology Service Provider Interface
COMPONENT_SRC=          $(COMPONENT_NAME)-$(COMPONENT_VERSION)
COMPONENT_ARCHIVE=      $(COMPONENT_SRC).tar.xz
COMPONENT_ARCHIVE_HASH= \
	sha256:1e90d064b937aacfe79a96232ac7e63d28d716e85bd9ff4333f865305a959b5b
COMPONENT_ARCHIVE_URL=  \
	https://download.gnome.org/sources/$(COMPONENT_NAME)/2.24/$(COMPONENT_ARCHIVE)
COMPONENT_PROJECT_URL=  http://www.gnome.org
COMPONENT_FMRI=         gnome/accessibility/at-spi2-core
COMPONENT_CLASSIFICATION=Desktop (GNOME)/Libraries
COMPONENT_LICENSE=      LGPLv2
COMPONENT_LICENSE_FILE= COPYING

TEST_TARGET=$(NO_TESTS)
include $(WS_MAKE_RULES)/common.mk

PATH=$(PATH.gnu)

CONFIGURE_OPTIONS += --sysconfdir=/etc
CONFIGURE_OPTIONS += --libexecdir=$(CONFIGURE_LIBDIR.$(BITS))
CONFIGURE_OPTIONS += --with-dbus_daemondir=/usr/lib
CONFIGURE_OPTIONS += --enable-xevie=no
CONFIGURE_OPTIONS.32 += --enable-introspection=no

CONFIGURE_ENV += PYTHON=$(PYTHON)
CONFIGURE_ENV += PERL=$(PERL)

COMPONENT_BUILD_ENV += CC="$(CC)"
COMPONENT_BUILD_ENV += CFLAGS="$(CFLAGS)"

$(INSTALL_32):	$(INSTALL_64)

REQUIRED_PACKAGES += library/perl-5/xml-parser
# Auto-generated dependencies
REQUIRED_PACKAGES += library/glib2
REQUIRED_PACKAGES += system/library
REQUIRED_PACKAGES += system/library/libdbus
REQUIRED_PACKAGES += x11/library/libx11
REQUIRED_PACKAGES += x11/library/libxtst
