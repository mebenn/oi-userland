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
# Copyright 2016 Aurelien Larcher
#

X11_CATEGORY=LIB
include ../../../make-rules/shared-macros.mk
include $(WS_MAKE_RULES)/x11.mk

COMPONENT_NAME=    libSM
COMPONENT_VERSION= 1.2.4
COMPONENT_SUMMARY= libSM - Session Management library 
COMPONENT_ARCHIVE_EXTENSION= .tar.xz
COMPONENT_ARCHIVE_HASH= sha256:fdcbe51e4d1276b1183da77a8a4e74a137ca203e0bcfb20972dd5f3347e97b84
COMPONENT_FMRI=    x11/library/libsm

include $(WS_MAKE_RULES)/common.mk

CONFIGURE_OPTIONS+= --disable-static
CONFIGURE_OPTIONS+= --enable-shared
CONFIGURE_OPTIONS+= --enable-unix-transport
CONFIGURE_OPTIONS+= --enable-tcp-transport
CONFIGURE_OPTIONS+= --enable-ipv6
CONFIGURE_OPTIONS+= --without-libuuid

LD_OPTIONS = -M $(PWD)/mapfile-vers

# Build dependencies
REQUIRED_PACKAGES += x11/library/xtrans

# Auto-generated dependencies
REQUIRED_PACKAGES += system/library
REQUIRED_PACKAGES += x11/library/libice
