{ jacobi ? import
    (
      fetchTarball {
        name = "jpetrucciani-2023-01-10";
        url = "https://github.com/jpetrucciani/nix/archive/23f89522981c885478b8d149b45422200188b523.tar.gz";
        sha256 = "0p6mz1mm9p6ywvjnhc3ffv11f343hpgznqagrrhnnzhxa4hmd0zp";
      }
    )
    { }
}:
let
  inherit (jacobi.hax) ifIsLinux ifIsDarwin;

  name = "website";
  tools = with jacobi; {
    cli = [
      jq
      nixpkgs-fmt
    ];
    python = [ (python310.withPackages (p: with p; [ 
      requests
      python-dotenv
      atlassian-python-api
      jira
      js2py
      flask
      django
      
      ])) ];
  };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
