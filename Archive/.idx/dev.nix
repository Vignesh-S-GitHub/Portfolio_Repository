# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Full
    pkgs.docker-compose
    pkgs.chromedriver
  ];

  # Sets environment variables in the workspace
  env = {
    LD_LIBRARY_PATH = "/nix/store/mpcnljkmd6r804wnvj3gdcms9d4ffyjf-libxcb-1.17.0/lib:$LD_LIBRARY_PATH:/nix/store/1pq1qp7awv4jxxbap0fc9h8ndcm8r0y5-nspr-4.36/lib:$LD_LIBRARY_PATH:/nix/store/i0j1kwy3k7ds8g3463438ihlr4x2h08p-nss-3.101.2/lib:$LD_LIBRARY_PATH:/nix/store/xxy06s17mvjm6x43cjp0zysrr3va674q-glib-2.80.2/lib:$LD_LIBRARY_PATH";
  };
    services.docker = {
    enable = true;
  };
  services.postgres = {
  enable = true;
  package = pkgs.postgresql;
  };
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      # "vscodevim.vim"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        # web = {
        #   # Example: run "npm run dev" with PORT set to IDX's defined port for previews,
        #   # and show it in IDX's web preview panel
        #   command = ["streamlit" "run" "stock_tracker.py"];
        #   manager = "web";
        #   env = {
        #     # Environment variables to set for your server
        #     PORT = "$PORT";
        #   };
        # };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Example: install JS dependencies from NPM
        # npm-install = "npm install";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task to watch and re-build backend code
        # venv_start = "source /home/user/Portfolio_Repository/.venv/bin/activate";
      };
    };
  };
}
