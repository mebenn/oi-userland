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
# Copyright 2018, cgrzemba@opencsw.org
# Copyright 2018, Aurelien Larcher
# Copyright 2018, Michal Nowak
# Copyright 2021, Carsten Grzemba
# Copyright 2023,2024 Friedrich Kink
#

# This build is a mixture of configure and python style
# it starts with configure for the initial setup 
# the compiler build itself is intensively using python tools
# therefor this patially python settings

TEST_STYLE=		none

include ../../../make-rules/shared-macros.mk

COMPONENT_NAME=		rustc
COMPONENT_VERSION=	1.75.0
COMPONENT_SUMMARY=	Rust - Safe, concurrent, practical language
COMPONENT_PROJECT_URL=	https://www.rust-lang.org
COMPONENT_SRC=		$(COMPONENT_NAME)-$(COMPONENT_VERSION)-src
COMPONENT_ARCHIVE=	$(COMPONENT_SRC).tar.gz
COMPONENT_ARCHIVE_HASH=	sha256:5b739f45bc9d341e2d1c570d65d2375591e22c2d23ef5b8a37711a0386abc088
COMPONENT_ARCHIVE_URL=	https://static.rust-lang.org/dist/$(COMPONENT_ARCHIVE)
COMPONENT_FMRI=		developer/lang/rustc
COMPONENT_CLASSIFICATION=	Development/Other Languages
COMPONENT_LICENSE=	MIT or Apache-2.0
COMPONENT_LICENSE_FILE=	LICENSE-APACHE

RUST_BOOTSTRAP_PATH=	$(BUILD_DIR)/$(MACH64)
RUST_ARCH=		x86_64-unknown-illumos

TEST_TARGET=		$(NO_TESTS)

include $(WS_MAKE_RULES)/common.mk
include $(WS_MAKE_RULES)/setup.py.mk

CLANG_VERSION=		17

# Need some help to pick the correct ar binary
GNUAR=$(GNUBIN)/ar

# Put the bits cargo downloads in a private directory.  This could be cached
# somewhere more permanent, but it's important to make sure that a person's
# $HOME/.cargo isn't used.
CARGO_HOME=             $(@D)/.cargo

PATH=                   $(PATH.gnu)

RUSTC_BIN_POST=		cargo
RUSTC_BIN_POST+=	clippy-driver
RUSTC_BIN_POST+=	rls
RUSTC_BIN_POST+=	rustc
RUSTC_BIN_POST+=	rustdoc

# Add arch triplet to pkg macros
PKG_MACROS+=		RUST_ARCH="$(RUST_ARCH)"

# Rust expects the library path to be /usr/lib and is broken otherwise 
RUSTC_LIBDIR=		$(USRLIBDIR)

COMPONENT_PRE_CONFIGURE_ACTION += ( CLONEY_MODE=hardlink $(CLONEY) $(SOURCE_DIR) $(@D); )

CONFIGURE_OPTIONS = --prefix=$(CONFIGURE_PREFIX)
CONFIGURE_OPTIONS += --mandir=$(CONFIGURE_MANDIR)
CONFIGURE_OPTIONS += --bindir=$(CONFIGURE_BINDIR.$(BITS))
CONFIGURE_OPTIONS += --libdir=$(RUSTC_LIBDIR)
CONFIGURE_OPTIONS += --docdir=$(USRSHAREDOCDIR)/rust-$(COMPONENT_VERSION)
CONFIGURE_OPTIONS += --datadir=$(USRSHAREDIR)
CONFIGURE_OPTIONS += --sysconfdir=$(ETCDIR)
CONFIGURE_OPTIONS += --enable-local-rust
CONFIGURE_OPTIONS += --local-rust-root=/usr
CONFIGURE_OPTIONS += --enable-extended       # Build and install cargo too.
CONFIGURE_OPTIONS += --default-linker=$(CC)
CONFIGURE_OPTIONS += --set target.$(RUST_ARCH).cc=$(CC)
CONFIGURE_OPTIONS += --set target.$(RUST_ARCH).cxx=$(CXX)
CONFIGURE_OPTIONS += --set target.$(RUST_ARCH).ar=$(GNUAR)
CONFIGURE_OPTIONS += --set target.$(RUST_ARCH).linker=$(CC)
CONFIGURE_OPTIONS += --enable-rpath
CONFIGURE_OPTIONS += --disable-codegen-tests
CONFIGURE_OPTIONS += --disable-dist-src
CONFIGURE_OPTIONS += --disable-llvm-static-stdcpp
CONFIGURE_OPTIONS += --enable-vendor
CONFIGURE_OPTIONS += --disable-docs
CONFIGURE_OPTIONS += --disable-compiler-docs
CONFIGURE_OPTIONS += --disable-cargo-native-static
CONFIGURE_OPTIONS += --enable-option-checking
CONFIGURE_OPTIONS += --release-channel=stable
CONFIGURE_OPTIONS += --python=$(PYTHON)
CONFIGURE_OPTIONS += --disable-clang
CONFIGURE_OPTIONS += --enable-llvm-link-shared
CONFIGURE_OPTIONS += --llvm-root=$(CLANG_PREFIX)
CONFIGURE_OPTIONS += --llvm-config=$(CLANG_PREFIX)/bin

COMPONENT_BUILD_CMD = $(PYTHON) x.py build 
COMPONENT_INSTALL_CMD = $(PYTHON) x.py install
COMPONENT_INSTALL_ARGS =

# Cleanup standard environment!
COMPONENT_BUILD_ENV =
COMPONENT_BUILD_ENV += OPENSSL_DIR=$(OPENSSL_PREFIX)
COMPONENT_BUILD_ENV += OPENSSL_LIB_DIR=$(OPENSSL_LIBDIR)
COMPONENT_BUILD_ENV += OPENSSL_INCLUDE_DIR=$(OPENSSL_INCDIR)
COMPONENT_BUILD_ENV += OPENSSL_STATIC=0
COMPONENT_BUILD_ENV += CC=$(CC)
COMPONENT_BUILD_ENV += CFLAGS="$(CFLAGS)"
COMPONENT_BUILD_ENV += CXX=$(CXX)
COMPONENT_BUILD_ENV += CXXFLAGS="$(CXXFLAGS)"
COMPONENT_BUILD_ENV += AR=$(GNUAR)
COMPONENT_BUILD_ENV += RUSTC=/usr/bin/rustc
COMPONENT_BUILD_ENV += CARGO_HOME=$(CARGO_HOME)
COMPONENT_BUILD_ENV += GMAKE=
# Enforce linker consistency
COMPONENT_BUILD_ENV +=	RUSTFLAGS="-C linker=$(CC)"
COMPONENT_BUILD_ENV +=	RUST_BACKTRACE=1

COMPONENT_PRE_INSTALL_ACTION = mkdir -p $(PROTO_DIR)
COMPONENT_POST_INSTALL_ACTION +=  $(TOUCH) $(BUILD_DIR)/META.depend-runtime.res

# Cleanup standard environment
COMPONENT_INSTALL_ENV= 
COMPONENT_INSTALL_ENV+=	$(COMPONENT_BUILD_ENV)
COMPONENT_INSTALL_ENV+=	CARGO_HOME=$(CARGO_HOME)
# Set install path
COMPONENT_INSTALL_ENV+=	DESTDIR=$(PROTO_DIR)

# manually added dependencies
REQUIRED_PACKAGES += developer/lang/rustc # previous before build version

# Auto-generated dependencies
PYTHON_REQUIRED_PACKAGES += runtime/python
REQUIRED_PACKAGES += $(GCC_RUNTIME_PKG)
REQUIRED_PACKAGES += $(GXX_RUNTIME_PKG)
REQUIRED_PACKAGES += library/libgit2
REQUIRED_PACKAGES += library/security/openssl-31
REQUIRED_PACKAGES += library/zlib
REQUIRED_PACKAGES += shell/ksh93
REQUIRED_PACKAGES += system/library
REQUIRED_PACKAGES += system/library/math
REQUIRED_PACKAGES += web/curl
