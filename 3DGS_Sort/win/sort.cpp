#include <iostream>
#include <windows.h>
#include <cstdlib>  
#include <string> 
#include <vector>
#include <regex>

std::vector<std::string> splitBySpace(const std::string& str) {
    std::vector<std::string> tokens;
    std::regex re("\\s+");  
    std::sregex_token_iterator it(str.begin(), str.end(), re, -1);
    std::sregex_token_iterator end;

    while (it != end) 
    {
        tokens.push_back(*it++);
    }

    return tokens;
}

void sort(int splatCount , int* splatID , float* camera , float* center)
{
    float x = 0.0;
    float y = 0.0;
    float z = 0.0;
    float w = 0.0;

    float bound_min_x = center[0];
    float bound_min_y = center[1];
    float bound_min_z = center[2];
    float bound_max_x = center[0];
    float bound_max_y = center[1];
    float bound_max_z = center[2];

    // Calculate bounding box of all vertices
    for (int i = 0; i < splatCount; i++)
    {
        x = center[i * 3 + 0];
        y = center[i * 3 + 1];
        z = center[i * 3 + 2];
        bound_min_x = min(bound_min_x, x);
        bound_min_y = min(bound_min_y, y);
        bound_min_z = min(bound_min_z, z);
        bound_max_x = max(bound_max_x, x);
        bound_max_y = max(bound_max_y, y);
        bound_max_z = max(bound_max_z, z);
    }


    int compareBits = 16;
    int bucketCount = pow(2, compareBits) + 1;
    int* distances = (int*)malloc(splatCount * sizeof(int));
    int* countBuffer = (int*)malloc(bucketCount * sizeof(int));
    memset(countBuffer, 0, bucketCount * sizeof(int));

    // Calculate min / max distance between camera and bounding box
    float d = 0.0;
    float px = camera[0];
    float py = camera[1];
    float pz = camera[2];
    float dx = camera[3];
    float dy = camera[4];
    float dz = camera[5];
    float min_dist = 0.0;
    float max_dist = 0.0;

    for (int i = 0; i < 8; i++)
    {
        x = i & 1 ? bound_min_x : bound_max_x;
        y = i & 2 ? bound_min_y : bound_max_y;
        z = i & 4 ? bound_min_z : bound_max_z;
        d = (x - px) * dx + (y - py) * dy + (z - pz) * dz;
        if (i == 0)
        {
            min_dist = d;
            max_dist = d;
        }
        else
        {
            min_dist = min(min_dist, d);
            max_dist = max(max_dist, d);
        }
    }


    float range_dist = max_dist - min_dist + 1e-7;
    float divider = (1 / range_dist) * pow(2, compareBits);
    int sort_key = 0;
    int istride = 0;
    for (int i = 0; i < splatCount; i++)
    {
        istride = i * 3;
        d = (center[istride + 0] - px) * dx + (center[istride + 1] - py) * dy + (center[istride + 2] - pz) * dz;
        sort_key = int((d - min_dist) * divider);
        distances[i] = sort_key;

        countBuffer[sort_key]++;
    }

    for (int i = 1; i < bucketCount; i++)
    {
        countBuffer[i] += countBuffer[i - 1];
    }

    int distance = 0;
    for (int i = splatCount - 1; i >= 0; i--)
    {
        distance = distances[i];
        splatID[countBuffer[distance] - 1] = i;
        countBuffer[distance]--;
    }

    free(distances);
    free(countBuffer);
}

int main(int argc, char* argv[])
{
    std::string input;
    std::vector<std::string> result;
    while (1)
    {
        std::getline(std::cin , input);
        result = splitBySpace(input);

        /*
        result format
        0 -   command  
        1 -   splat_count
        2 -   splatID_shm name
        3 -   camera_shm name
        4 -   center_shm name
        */
        
        if (result[0] == "0")
        {
            //sort
            int splat_count = std::stoi(result[1]);
            size_t shm_size = 0;

            //splatID
            HANDLE splatIDMapFile = OpenFileMappingA(FILE_MAP_ALL_ACCESS, FALSE, result[2].c_str());

            if (splatIDMapFile == NULL)
            {
                std::cerr << "fail to open shared memory: " << result[2] << std::endl;
                exit(1);
            }

            shm_size = splat_count * sizeof(int);

            void* splatIDMapFileBuf = MapViewOfFile(splatIDMapFile, FILE_MAP_ALL_ACCESS, 0, 0, shm_size);
            int* splatID = static_cast<int*>(splatIDMapFileBuf);

            //camera
            HANDLE cameraMapFile = OpenFileMappingA(FILE_MAP_ALL_ACCESS, FALSE, result[3].c_str());

            if (cameraMapFile == NULL)
            {
                std::cerr << "fail to open shared memory: " << result[3] << std::endl;
                exit(1);
            }

            shm_size = 6 * sizeof(float);

            void* cameraMapFileBuf = MapViewOfFile(cameraMapFile, FILE_MAP_ALL_ACCESS, 0, 0, shm_size);
            float* camera = static_cast<float*>(cameraMapFileBuf);

            //center
            HANDLE centerMapFile = OpenFileMappingA(FILE_MAP_ALL_ACCESS, FALSE, result[4].c_str());

            if (centerMapFile == NULL)
            {
                std::cerr << "fail to open shared memory: " << result[4] << std::endl;
                exit(1);
            }

            shm_size = splat_count * 3  * sizeof(float);

            void* centerMapFileBuf = MapViewOfFile(centerMapFile, FILE_MAP_ALL_ACCESS, 0, 0, shm_size);
            float* center = static_cast<float*>(centerMapFileBuf);

            sort(splat_count, splatID, camera, center);
            std::cout << "1" << std::endl;
            
        }
    }
    
    return 0;
}

