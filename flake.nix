{
  description = "Comparación de compresión Wavelet vs JPEG";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          numpy
          pywavelets
          pillow
          pandas
          scikit-image
          tabulate
          matplotlib
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.python311Packages.pip
          ];

          shellHook = ''
            echo "🌊 Entorno Wavelet vs JPEG activado"
            echo "Python: $(python --version)"
            echo ""
            echo "Para ejecutar el análisis:"
            echo "  python main.py"
            echo "  python main.py --image ruta/imagen.png"
            echo ""
          '';
        };

        packages.default = pkgs.writeShellScriptBin "wavelet-compare" ''
          ${pythonEnv}/bin/python ${./main.py}
        '';

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/wavelet-compare";
        };
      }
    );
}

