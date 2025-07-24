import os

def create_project_structure():
    project_name = "eventos_igreja"
    structure = {
        f"{project_name}/": ["main.py", "requirements.txt", "README.md"],
        f"{project_name}/src/": ["__init__.py"],
        f"{project_name}/src/database/": ["__init__.py", "db_manager.py", "schema.sql"],
        f"{project_name}/src/models/": ["__init__.py", "participant.py"],
        f"{project_name}/src/services/": ["__init__.py", "participant_service.py"],
        f"{project_name}/src/ui/": ["__init__.py", "main_window.py"],
    }

    for folder, files in structure.items():
        os.makedirs(folder, exist_ok=True)
        for file in files:
            with open(os.path.join(folder, file), "w") as f:
                f.write("")  # Cria arquivos vazios

if __name__ == "__main__":
    create_project_structure()
    print("Estrutura do projeto 'eventos_igreja' criada com sucesso!")