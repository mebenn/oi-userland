#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2011, 2016, Oracle and/or its affiliates. All rights reserved.
# Copyright (c) 2018, Michal Nowak
#

BUILD_STYLE=configure
BUILD_BITS=64
include ../../../make-rules/shared-macros.mk
include $(WS_MAKE_RULES)/shared-targets.mk

COMPONENT_NAME=         zsh
COMPONENT_VERSION=      5.9
COMPONENT_PROJECT_URL=  https://www.zsh.org/
COMPONENT_SRC=          $(COMPONENT_NAME)-$(COMPONENT_VERSION)
COMPONENT_ARCHIVE=      $(COMPONENT_SRC).tar.xz
COMPONENT_ARCHIVE_HASH= sha256:9b8d1ecedd5b5e81fbf1918e876752a7dd948e05c1a0dba10ab863842d45acd5
COMPONENT_ARCHIVE_URL=  https://downloads.sourceforge.net/project/zsh/zsh/$(COMPONENT_VERSION)/$(COMPONENT_ARCHIVE)
COMPONENT_SIG_URL=	$(COMPONENT_ARCHIVE_URL).asc
COMPONENT_CLASSIFICATION=	System/Shells
COMPONENT_FMRI=         shell/zsh

include $(WS_MAKE_RULES)/common.mk

# Force help files regeneration
COMPONENT_POST_UNPACK_ACTION = ($(RM) $(SOURCE_DIR)/Doc/help.txt)

CONFIGURE_LIBDIR.64= $(USRLIBDIR)

CONFIGURE_OPTIONS += -n
CONFIGURE_OPTIONS += --enable-cppflags="$(CPP_LARGEFILES)"
CONFIGURE_OPTIONS += --enable-cap
CONFIGURE_OPTIONS += --enable-dynamic
CONFIGURE_OPTIONS += --enable-etcdir=/etc
CONFIGURE_OPTIONS += --enable-function-subdirs
# Zsh uses the compiler to link, so we need to pass CC_BITS, not LD_BITS.
CONFIGURE_OPTIONS += --enable-ldflags="$(CC_BITS) -zignore"
CONFIGURE_OPTIONS += --enable-libs="-lnsl"
CONFIGURE_OPTIONS += --enable-maildir-support
CONFIGURE_OPTIONS += --enable-multibyte
CONFIGURE_OPTIONS += --enable-pcre
CONFIGURE_OPTIONS += --with-tcsetpgrp
CONFIGURE_OPTIONS += --disable-gdbm

COMPONENT_POST_CONFIGURE_ACTION = (cd $(@D); ./config.status)

COMPOVERRIDES = $(shell test -d Completion && find Completion -type f -print)

$(PROTOETCDIR)/%: % $(PROTOETCDIR)
	$(INS.file)

$(PROTOETCDIR)/zprofile: $(PROTOETCDIR)
	$(RM) $@; $(SYMLINK) profile $@

# The configure test for NIS tests to make sure that NIS is working, not whether
# it's available to compile against. We actually want to go through the switch
# in all cases, so we force it off, regardless of whether the build environment
# has it enabled.
CONFIGURE_ENV += zsh_cv_sys_nis=no

$(COMPONENT_SRC)/Completion/%: Completion/%
	$(CP) $< $@

$(COMPONENT_SRC)/LICENCE: prep

license: $(COMPONENT_SRC)/LICENCE
	tail +13 $< > $@

CLEAN_PATHS += license

COMPONENT_POST_INSTALL_ACTION = find $(PROTO_DIR) -name '*.~1~' -exec rm {} \;

COMPONENT_TEST_ENV += PATH=$(PATH.gnu)

# common targets
build:		$(BUILD_64) $(COMPOVERRIDES:%=$(COMPONENT_SRC)/%)

install:	build $(INSTALL_64) $(PROTOETCDIR)/zprofile $(PROTOETCDIR)/zshrc license

# build does this always

# Auto-generated dependencies
REQUIRED_PACKAGES += library/ncurses
REQUIRED_PACKAGES += library/pcre
REQUIRED_PACKAGES += system/library
REQUIRED_PACKAGES += system/library/math
