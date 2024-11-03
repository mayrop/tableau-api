"""Entrypoint for the app"""
import tableauserverclient as TSC
import os
import argparse

from dotenv import load_dotenv

load_dotenv()


# TODO - error handling
def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--view_name", required=True, help="Name of the view to search for"
    )
    return parser


def find_view_by_name(view_name: str) -> None:
    """Main function"""
    tableau_auth = TSC.TableauAuth(
        os.getenv("USER"), os.getenv("PASSWORD"), os.getenv("SITENAME")
    )
    server_url = os.getenv("SERVER_URL")
    server = TSC.Server(server_url)

    def is_name_match(view, target):
        return target.lower() in view.name.lower()

    filtered = []
    with server.auth.sign_in(tableau_auth):
        for view in TSC.Pager(server.views):
            if not is_name_match(view, view_name):
                continue

            workbook = server.workbooks.get_by_id(view.workbook_id).name
            project = "No project"

            if view.project_id:
                project = server.projects.get_by_id(view.project_id).name

            filtered.append(
                {
                    "id": view.id,
                    "name": view.name,
                    "workbook": workbook,
                    "project": project,
                    "url": f"{server_url}{view.content_url}",
                }
            )

    if filtered:
        print(f"Found {len(filtered)} views matching '{view_name}'\n\n")

        for view in filtered:
            print(f"View ID: {view['id']}")
            print(f"View Name: {view['name']}")
            print(f"Workbook: {view['workbook']}")
            print(f"Project: {view['project']}")
            print(f"View URL: {view['url']}")
            print("\n\n")


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    find_view_by_name(view_name=args.view_name)


if __name__ == "__main__":
    main()
