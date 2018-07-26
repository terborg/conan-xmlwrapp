
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
    
    exports = "config.*"
    
    def source(self):

        tools.get( "https://github.com/vslavik/xmlwrapp/releases/download/v0.9.0/xmlwrapp-0.9.0.tar.gz", 
                   sha1="6fa3193a013b7d29bb22e220e9bd015bc14eb11e" )
        
        #
        # Here, we upgrade the config.guess and config.sub, because they are way too old
        #
        self.run( 'cp -v ' + os.path.dirname( os.path.realpath(__file__) ) + '/config.* ' + os.path.join( self.source_path(), 'admin/' ) )

    def source_path( self ):
        return os.path.join( self.source_folder, self.name + '-' + self.version )

    def build(self):

        if self.settings.os == "Android" and self.settings.compiler == "clang":        
            del self.settings.compiler.libcxx

        env_build = AutoToolsBuildEnvironment(self)
        use_vars = env_build.vars

        #
        # the configure script needs extra motivation not to resort to the default /usr/include stuff
        #
        if 'libxml2' in self.deps_cpp_info.deps:
            libxml2_info = self.deps_cpp_info[ 'libxml2' ]
            use_vars[ 'LIBXML_CFLAGS' ] = '-I' + libxml2_info.include_paths[0]
            use_vars[ 'LIBXML_LIBS' ] = '-lxml2'
            
        configure_args = [ '--disable-docs', '--disable-tests', '--disable-xslt' ]
        if not self.options.shared:
            configure_args.extend( [ '--enable-static', '--disable-shared', '--enable-static-boost' ] )
            
        if self.options.fPIC:
            configure_args.extend( [ '--with-pic' ] )
        
        env_build.configure( configure_dir = self.source_path(), args=configure_args, vars=use_vars )
        env_build.make( vars=use_vars )

    def package(self):
        
        self.copy( "*.h", dst="include", src= os.path.join( self.source_path(), "include" )  )
        
        self.copy( "*xmlwrapp.lib", dst="lib", keep_path=False )
        self.copy( "*.dll", dst="bin", keep_path=False )
        self.copy( "*.so", dst="lib", keep_path=False )
        self.copy( "*.dylib", dst="lib", keep_path=False )
        self.copy( "*.a", dst="lib", keep_path=False )

    def package_info(self):
        self.cpp_info.libs = ["xmlwrapp"]

