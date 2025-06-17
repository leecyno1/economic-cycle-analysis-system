#!/usr/bin/env python
"""
WindPy安装和配置脚本
自动安装WindPy并测试Wind数据库连接
"""
import os
import sys
import subprocess
import django
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

def install_windpy():
    """安装WindPy"""
    print("=" * 80)
    print("WindPy安装程序")
    print("=" * 80)
    
    print("\n🔍 检查WindPy安装状态...")
    
    try:
        import WindPy
        print("✅ WindPy已安装")
        return True
    except ImportError:
        print("❌ WindPy未安装，开始安装...")
        
        try:
            # 尝试通过pip安装WindPy
            print("📦 正在安装WindPy...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "WindPy"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ WindPy安装成功")
                return True
            else:
                print(f"❌ WindPy安装失败: {result.stderr}")
                
                # 提供手动安装指导
                print("\n💡 手动安装WindPy步骤:")
                print("1. 访问万得官网下载WindPy安装包")
                print("2. 运行安装程序并按指导完成安装")
                print("3. 或者尝试以下命令:")
                print("   pip install WindPy")
                print("   或")
                print("   conda install WindPy")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 安装超时，请检查网络连接")
            return False
        except Exception as e:
            print(f"❌ 安装过程中出现异常: {str(e)}")
            return False

def check_wind_requirements():
    """检查Wind环境要求"""
    print("\n🔍 检查Wind环境要求...")
    
    requirements = []
    
    # 检查操作系统
    import platform
    os_name = platform.system()
    if os_name == "Windows":
        print("✅ 操作系统: Windows (推荐)")
    elif os_name == "Darwin":
        print("⚠️  操作系统: macOS (部分功能可能受限)")
    else:
        print(f"⚠️  操作系统: {os_name} (可能不完全支持)")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version >= (3, 6):
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python版本过低: {python_version.major}.{python_version.minor} (需要3.6+)")
        requirements.append("升级Python到3.6或更高版本")
    
    # 检查必要的包
    required_packages = ['pandas', 'numpy']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")
            requirements.append(f"安装{package}: pip install {package}")
    
    if requirements:
        print("\n📋 需要满足以下要求:")
        for req in requirements:
            print(f"  • {req}")
        return False
    else:
        print("✅ 所有环境要求已满足")
        return True

def test_wind_setup():
    """测试Wind设置"""
    print("\n🔍 测试Wind数据库连接...")
    
    try:
        from data_hub.wind_data_collector import WindDataCollector, WindConnectionConfig
        
        # 创建Wind配置
        wind_config = WindConnectionConfig(
            username="17600806220",
            password="iv19whot"
        )
        
        # 创建Wind收集器
        collector = WindDataCollector(wind_config)
        
        # 测试连接
        connection_result = collector.test_connection()
        
        if connection_result['connected']:
            print("✅ Wind数据库连接成功!")
            print(f"   Wind版本: {connection_result.get('wind_version', '未知')}")
            print(f"   数据测试: {connection_result.get('test_data', '未测试')}")
            
            # 显示支持的指标
            supported_indicators = collector.get_supported_indicators()
            print(f"   支持指标数量: {len(supported_indicators)}")
            
            return True
        else:
            print(f"❌ Wind数据库连接失败: {connection_result['error_message']}")
            
            # 提供故障排除建议
            print("\n💡 故障排除建议:")
            print("1. 确保Wind客户端已安装并登录")
            print("2. 检查用户名和密码是否正确")
            print("3. 确认网络连接正常")
            print("4. 联系Wind客户服务")
            
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {str(e)}")
        return False

def create_wind_config_file():
    """创建Wind配置文件"""
    print("\n📝 创建Wind配置文件...")
    
    config_content = '''# -*- coding: utf-8 -*-
"""
Wind数据库配置文件
包含连接参数和常用设置
"""

# Wind连接配置
WIND_CONFIG = {
    'username': '17600806220',
    'password': 'iv19whot',
    'timeout': 60,
    'retry_times': 3,
    'retry_delay': 5
}

# Wind指标优先级配置
WIND_PRIORITY_INDICATORS = [
    'WIND_CPI_YOY',
    'WIND_PPI_YOY', 
    'WIND_GDP_YOY',
    'WIND_M2_YOY',
    'WIND_PMI_MFG',
    'WIND_CSI300',
    'WIND_10Y_TREASURY'
]

# Wind数据质量要求
WIND_QUALITY_CONFIG = {
    'min_data_points': 10,
    'max_missing_ratio': 0.1,
    'outlier_threshold': 3.0
}
'''
    
    try:
        with open('wind_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Wind配置文件创建成功: wind_config.py")
        return True
    except Exception as e:
        print(f"❌ 创建配置文件失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("WindPy环境配置助手")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查环境要求
    if not check_wind_requirements():
        print("\n❌ 环境检查失败，请先满足基本要求")
        return False
    
    # 安装WindPy
    if not install_windpy():
        print("\n❌ WindPy安装失败")
        return False
    
    # 创建配置文件
    create_wind_config_file()
    
    # 测试Wind连接
    if test_wind_setup():
        print("\n🎉 Wind环境配置完成!")
        print("\n📋 下一步操作:")
        print("1. 运行: python test_wind_connection.py")
        print("2. 运行: python manage.py collect_wind_data --test-connection")
        print("3. 收集数据: python manage.py collect_wind_data --years 1")
        return True
    else:
        print("\n⚠️  Wind环境配置部分完成，但连接测试失败")
        print("请检查Wind客户端和网络连接后重试")
        return False

if __name__ == "__main__":
    main() 