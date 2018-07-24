
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class XMLWrappConan(ConanFile):
    name = "xmlwrapp"
    version = "0.9.0"
    license = "BSD 3-clause"
    url = "https://github.com/vslavik/xmlwrapp"
    description = "Lightweight C++ XML parsing library"
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    requires = (
            "libxml2/2.9.8@bincrafters/stable",
            "boost/1.67.0@conan/stable"
        )
    source_subfolder = name + '-' + version
    
    def source(self):
        tools.get( "https://github.com/vslavik/xmlwrapp/releases/download/v0.9.0/xmlwrapp-0.9.0.tar.gz", 
                   sha1="6fa3193a013b7d29bb22e220e9bd015bc14eb11e" )

    def source_path( self ):
        return os.path.join( self.source_folder, self.name + '-' + self.version )

    def build(self):
        
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.fPIC
        
        configure_args = [ '--disable-docs', '--disable-tests' ]
        if not self.options.shared:
            configure_args.extend( [ '--enable-static', '--disable-shared', '--enable-static-boost' ] )
        
        env_build.configure( configure_dir = self.source_path(), args=configure_args )
        env_build.make()

    def package(self):
        
        self.copy( "*.h", dst="include", src= os.path.join( self.source_path(), "include" )  )
        
        self.copy( "*xmlwrapp.lib", dst="lib", keep_path=False )
        self.copy( "*.dll", dst="bin", keep_path=False )
        self.copy( "*.so", dst="lib", keep_path=False )
        self.copy( "*.dylib", dst="lib", keep_path=False )
        self.copy( "*.a", dst="lib", keep_path=False )

    def package_info(self):
        self.cpp_info.libs = ["xmlwrapp"]

