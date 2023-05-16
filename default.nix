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
      curl
      ngrok
      just
      bashInteractive_5
      gron
    ];
    python = [ (python310.withPackages (p: with p; [ 
      # http
      httpx
      requests
  
      # integrations
      atlassian-python-api
      jira
     

      # webserver
      fastapi
      uvicorn
      # general/text
      anybadge
      tabulate
      python-dotenv

      
      ])) ];
  };

  env = jacobi.enviro {
    inherit name tools;
  };
in
env
