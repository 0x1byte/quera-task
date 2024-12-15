"use client";
import { Container } from "@chakra-ui/react";
import { Box, SimpleGrid, Heading } from "@chakra-ui/react";
import { HStack } from "@chakra-ui/react";
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination";
import { Flex, Text, Card, Stack, Button } from "@chakra-ui/react";
import { DataListItem, DataListRoot } from "@/components/ui/data-list";
import { Toaster, toaster } from "@/components/ui/toaster";
import { Avatar } from "@/components/ui/avatar";
import Link from "next/link";
import { useRouter, useParams } from "next/navigation";
import { userInfo, userExists, getRepos } from "@/utils/requests";
import { useState, useEffect } from "react";

const UserInfoPage = () => {
  const { username } = useParams();
  const router = useRouter();
  const handleBack = () => {
    router.back();
  };

  const [user, setUser] = useState(null);
  const [repos, setRepos] = useState(null);
  const [page, setPage] = useState(1);
  const pageSize = 6;
  const startRange = (page - 1) * pageSize;
  const endRange = startRange + pageSize;

  const getUserInfo = async () => {
    try {
      const status = await userExists(username);
      if (status === 200) {
        const response = await userInfo(username);
        setUser(response);
        const response2 = await getRepos(username);
        response2.sort(
          (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
        );
        setRepos(response2);
      }
    } catch (error) {
      if (error.response.status === 404) {
        toaster.create({
          title: "User not found",
          status: "error",
          duration: 5000,
        });
        setUser("not found");
      } else {
        toaster.create({
          title: "Something went wrong",
          status: "error",
          duration: 5000,
        });
      }
    }
  };

  useEffect(() => {
    const fetchUserInfo = async () => {
      await getUserInfo();
    };

    if (user === null) {
      fetchUserInfo();
    }
  }, [user, router, username]);

  if (user === "not found") {
    return (
      <Container fluid>
        <Flex h="100vh" justifyContent="center" alignItems="center">
          <Card.Root width="md">
            <Card.Header>
              <Card.Title>
                <Text fontSize="3xl">Github User Info</Text>
              </Card.Title>
              <Card.Description>
                Search any github user and get their details
              </Card.Description>
            </Card.Header>
            <Card.Body>
              <Stack gap="4" w="full">
                <Text fontSize="2xl" fontWeight="bold">
                  404 - User not found
                </Text>
              </Stack>
            </Card.Body>
            <Card.Footer alignItems="center" justifyContent="center">
              <Button onClick={handleBack}>Back</Button>
            </Card.Footer>
          </Card.Root>
        </Flex>
      </Container>
    );
  }
  if (user !== null && repos !== null) {
    return (
      <Container fluid>
        <Flex justifyContent="center" alignItems="center">
          <Card.Root width="lg" height="full" mt="10" mb="10">
            <Card.Header>
              <Card.Title>
                <Text fontSize="3xl">Github User Info</Text>
              </Card.Title>
              <Card.Description>
                Search any github user and get their details
              </Card.Description>
            </Card.Header>
            <Card.Body>
              <Stack gap="4" w="full">
                <DataListRoot>
                  <Avatar size="2xl" src={user.avatar_url} />
                  <DataListItem label="Name" value={user.name} />
                  <DataListItem label="Username" value={user.login} />
                  <DataListItem label="Bio" value={user.bio} />
                  <DataListItem label="Followers" value={user.followers} />
                  <DataListItem label="Following" value={user.following} />
                  <DataListItem label="Location" value={user.location} />
                  <DataListItem
                    label="Blog"
                    value={
                      user.blog && (
                        <Link href={user.blog} target="_blank">
                          {user.blog}
                        </Link>
                      )
                    }
                  />
                </DataListRoot>
                <Stack
                  display="flex"
                  justifyContent="center"
                  alignItems="center"
                  p={6}
                >
                  <Heading as="h1" size="lg" textAlign="center">
                    User Repositories
                  </Heading>
                  <SimpleGrid columns="2" spacing={6}>
                    {repos.slice(startRange, endRange).map((repo, index) => (
                      <Box
                        key={index}
                        borderWidth="1px"
                        borderRadius="md"
                        p={4}
                        m={1}
                        boxShadow="md"
                      >
                        <Heading as="h3" size="md">
                          {repo.name}
                        </Heading>
                        <Text mt={2} fontSize="sm" color="gray.600">
                          Updated at:{" "}
                          {new Date(repo.updated_at).toLocaleString()}
                        </Text>
                      </Box>
                    ))}
                  </SimpleGrid>
                  <PaginationRoot
                    count={repos.length}
                    pageSize={pageSize}
                    page={page}
                    onPageChange={(e) => setPage(e.page)}
                    defaultPage={1}
                  >
                    <HStack>
                      <PaginationPrevTrigger />
                      <PaginationItems />
                      <PaginationNextTrigger />
                    </HStack>
                  </PaginationRoot>
                </Stack>
              </Stack>
            </Card.Body>
            <Card.Footer alignItems="center" justifyContent="center">
              <Button onClick={handleBack}>Back</Button>
            </Card.Footer>
          </Card.Root>
        </Flex>
        <Toaster />
      </Container>
    );
  }
  if (user === null) {
    return (
      <Container fluid>
        <Flex h="100vh" justifyContent="center" alignItems="center">
          <Card.Root width="md">
            <Card.Header>
              <Card.Title>
                <Text fontSize="3xl">Github User Info</Text>
              </Card.Title>
              <Card.Description>
                Search any github user and get their details
              </Card.Description>
            </Card.Header>
            <Card.Body>
              <Stack gap="4" w="full">
                <Text fontSize="2xl" fontWeight="bold">
                  Loading...
                </Text>
              </Stack>
            </Card.Body>
            <Card.Footer alignItems="center" justifyContent="center">
              <Button onClick={handleBack}>Back</Button>
            </Card.Footer>
          </Card.Root>
        </Flex>
      </Container>
    );
  }
};

export default UserInfoPage;
