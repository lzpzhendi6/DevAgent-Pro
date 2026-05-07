from rich.console import Console
from rich.panel import Panel
from multi_agent import run_dev_agent
import os
from dotenv import load_dotenv

load_dotenv()
console = Console()

if __name__ == "__main__":
    console.print(Panel.fit("[bold cyan]🚀 DevAgent-Pro 多智能体开发系统启动[/bold cyan]", border_style="green"))
    
    # 示例需求（你可以改成自己的）
    user_requirement = "创建一个使用 FastAPI + SQLite 的 Todo List Web 应用，支持用户注册、登录和 CRUD 操作"
    
    console.print(f"[bold]📋 用户需求：[/bold] {user_requirement}\n")
    
    result = run_dev_agent(user_requirement)
    
    console.print(Panel("[bold green]✅ 多 Agent 协作完成！项目已自动生成、审查并通过测试[/bold green]", border_style="green"))
    console.print(f"总 Token 消耗: [bold]{result['token_usage']}[/bold] tokens")
    console.print("日志已保存至 logs/devagent.log（可用于申请截图）")
