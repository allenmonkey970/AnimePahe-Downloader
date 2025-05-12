import sys
import mainSite
import downloadSite

def print_menu():
    print("\n==== AnimePahe Downloader Main ====")
    print("1. Generate download links from animepahe (search anime, get .txt)")
    print("2. Download video files from links file (.txt)")
    print("3. Exit")
    print("===================================")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("\n[+] Running AnimePahe search & link generator...\n")
            mainSite.main()
        elif choice == "2":
            print("\n[+] Running file downloader for generated links...\n")
            downloadSite.main()
        elif choice == "3":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()