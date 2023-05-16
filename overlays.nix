let
  pynixifyOverlay =
    self: super: {
      python39 = super.python39.override { inherit packageOverrides; };
      python310 = super.python310.override { inherit packageOverrides; };
    };

  packageOverrides = self: super: with self; {
    inherit (super.stdenv) isDarwin isAarch64 isNixOS;
    isM1 = isDarwin && isAarch64;
    isOldMac = isDarwin && !isAarch64;

    dnspython =
      if self.isDarwin then
        super.dnspython.overrideAttrs
          (_: {
            disabledTestPaths =
              [
                "tests/test_async.py"
                "tests/test_query.py"
                "tests/test_resolver.py"
                "tests/test_resolver_override.py"
              ];
          }) else super.dnspython;

    pydash = super.pydash.overrideAttrs (
      _: {
        disabledTests = [
          "test_delay"
        ];
      }
    );

    okta = buildPythonPackage rec {
      pname = "okta";
      version = "2.5.0";

      src = fetchPypi {
        inherit pname version;
        sha256 = "1sc8m2zacc5azp8hrxqk9gdkjgnbsgjicfzslvx9sz6y01ncp74x";
      };

      propagatedBuildInputs = [
        aiohttp
        flatdict
        pyyaml
        xmltodict
        yarl
        pycryptodome
        python-jose
        aenum
        pydash
        setuptools
      ];

      doCheck = false;

      meta = with lib; {
        description = "Python SDK for the Okta Management API";
        homepage = "https://github.com/okta/okta-sdk-python";
      };
    };

    flatdict = buildPythonPackage rec {
      pname = "flatdict";
      version = "4.0.1";

      src = fetchPypi {
        inherit pname version;
        sha256 = "0hk7y93px4c10byv3gkp9yi4c86iddmz0xmwksq1xlhysf7z0cnd";
      };

      doCheck = false;

      meta = with lib; { };
    };

    google-auth = super.google-auth.overrideAttrs (
      _: {
        disabledTestPaths = [
          "tests/crypt/test__cryptography_rsa.py"
          "tests/crypt/test_es256.py"
          "tests/transport/compliance.py"
          "tests/transport/test__mtls_helper.py"
          "tests/transport/test_requests.py"
          "tests/transport/test_urllib3.py"
          "tests/test_jwt.py"
        ];
      }
    );

    httplib2 = super.httplib2.overrideAttrs (
      _: {
        disabledTests = [
          "test_timeout_subsequent"
          "test_connection_close"
          "test_client_cert_password_verified"
        ];
      }
    );

  };
in
pynixifyOverlay
