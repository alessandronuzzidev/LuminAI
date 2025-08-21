from cmd import Cmd
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn

from controller.controller import Controller

from services.control_monitor_lib import control_monitor

class LuminAICommand(Cmd):
    intro = 'Welcome to LuminAI. Type help or ? to list commands.\n'
    prompt = '\n\033[33mLuminAI (Enter command)-> \033[0m'
  
    def __init__(self):
        super().__init__()
        self.console = Console()
        self.controller = Controller()
        
        
        completed, total = self.controller.get_progress()
        if total > 0 and completed < total:
            self.console.print("[bold yellow]Indexing in progress detected. Resuming progress...[/bold yellow]")
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                TextColumn("{task.completed}/{task.total}"),
                console=self.console
            ) as progress:
                progress_task = progress.add_task("Indexing files...", total=total)
                while completed < total:
                    completed, total = self.controller.get_progress()
                    progress.update(progress_task, completed=completed)
                    time.sleep(1)
            self.console.print("[bold green]Indexing finished.[/bold green]")
        self.controller.cancel_indexing()
        control_monitor("pause")
        
    def default(self, line):
        """Override unknown command handler"""
        self.console.print(f"[bold red]Unknown command:[/bold red] {line}")
        self.console.print("Type [cyan]help[/cyan] to see available commands.")

    def do_exit(self, arg):
        """Exit the LuminAI CLI."""
        print('Exiting LuminAI CLI.')
        control_monitor("resume")
        self.controller.cancel_indexing()
        return True

    def do_help(self, arg):
        """List available commands."""
        table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("exit", "Exit the LuminAI CLI.")
        table.add_row("clear", "Clear the console.")
        table.add_row("config", "Show current configuration details.")
        table.add_row("configure_path <path>", "Configure the path for the file loader.")
        table.add_row("activate_rag_in_search", "Activate RAG in semantic search.")
        table.add_row("deactivate_rag_in_search", "Deactivate RAG in semantic search.")
        table.add_row("set_similarity_threshold <0-1>", "Set the similarity threshold for semantic search.")
        table.add_row("restart", "Restart the chat interface.")
        table.add_row("search <message>", "Generate a response based on the provided message.")

        self.console.print(table)
        
    def do_config(self, arg):
        """Show configuration details."""
        config_file = self.controller.load_config_file()
        if config_file:
            panel = Panel(Text(f"Configuration:\nPath: {config_file['path']}\nRAG Enabled: {config_file['checkbox_rag_value']}\nSimilarity Threshold: {config_file['similarity_threshold_value']}"), title="Current Configuration", border_style="blue")
            self.console.print(panel)
        else:
            self.console.print("[bold red]Error:[/bold red] Configuration file not found.")
        
    def do_configure_path(self, path):
        config_file = self.controller.load_config_file()
        if config_file["path"] == path:
            self.console.print("[bold red]Path is already set to the specified value.[/bold red]")
            return

        self.controller.update_path(path)
        self.console.print(f"Path updated to: [bold green]{path}[/bold green]")
        
        self.controller.index_documents()
        total_docs = self.controller.get_total_documents()
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=self.console
        ) as progress:
            progress_task = progress.add_task("Indexing files...", total=total_docs)
            while True:
                completed, total = self.controller.get_progress()
                progress.update(progress_task, completed=completed)
                if completed >= total:
                    break
                time.sleep(1)
            self.controller.cancel_indexing()

        self.console.print("[bold green]Indexing finished.[/bold green]")
                
    def do_activate_rag_in_search(self, arg):
        """Activate RAG in semantic search."""
        config_file = self.controller.load_config_file()
        self.controller.update_config_document(path=config_file["path"], checkbox_rag_value=True, similarity_threshold_value=config_file["similarity_threshold_value"])
        self.console.print("[bold green]RAG activated in semantic search[/bold green]")
        
    def do_deactivate_rag_in_search(self, arg):
        """Deactivate RAG in semantic search."""
        config_file = self.controller.load_config_file()
        self.controller.update_config_document(path=config_file["path"], checkbox_rag_value=False, similarity_threshold_value=config_file["similarity_threshold_value"])
        self.console.print("[bold green]RAG deactivated in semantic search[/bold green]")
        
    def do_set_similarity_threshold(self, threshold):
        """Set the similarity threshold for semantic search."""
        try:
            threshold_value = float(threshold)
            if 0 <= threshold_value <= 1:
                config_file = self.controller.load_config_file()
                self.controller.update_config_document(path=config_file["path"], checkbox_rag_value=config_file["checkbox_rag_value"], similarity_threshold_value=threshold_value)
                self.console.print(f"[bold green]Similarity threshold set to: {threshold_value}[/bold green]")
            else:
                self.console.print("[bold red]Error:[/bold red] Threshold must be between 0 and 1.")
        except ValueError:
            self.console.print("[bold red]Error:[/bold red] Invalid threshold value. Please enter a number between 0 and 1.")
        
    def do_restart(self, arg):
        """Restart the chat interface."""
        self.controller.restart_chat()
        self.console.print("[bold green]Chat interface restarted.[/bold green]")
        self.console.clear()
        
    def do_clear(self, arg):
        """Clear the self.console."""
        self.console.clear()
        
    def do_search(self, message):
        """Generate a response based on the provided message."""
        if not message:
            self.console.print("[bold red]Error:[/bold red] No message provided.")
            return
        self.console.print(f"[bold cyan]Searching...[/bold cyan]")
        response = self.controller.generate_response(message)
        if response:
            self.console.print(f"{response}")
        else:
            self.console.print("[bold red]Error:[/bold red] Failed to generate response.")
    
        
if __name__ == "__main__":
    LuminAICommand().cmdloop()